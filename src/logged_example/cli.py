#!/usr/bin/env python
from __future__ import print_function
import ctypes
from datetime import datetime
import os
import re
import signal
import shutil
from subprocess import Popen, PIPE
import signal
import sys
import tarfile

# Compatibility for Python 2 and 3
try:
    basestring
except NameError:
    basestring = str

class Sudoer:
    """Class to check for sudo privileges."""
    
    CLASSNAME = "Sudoer"
    MAJOR_VERSION = 1
    MINOR_VERSION = 1
    PATCH_VERSION = 8
    __is_root__ = None  # Cache for root status
    __is_sudo__ = None  # Cache for sudo status
    __handle_signal__ = None

    @staticmethod
    def class_version():
        """Return the class name and version string."""
        return f"{Sudoer.CLASSNAME} v{Sudoer.MAJOR_VERSION}.{Sudoer.MINOR_VERSION}.{Sudoer.PATCH_VERSION}"

    @staticmethod
    def root_or_sudo():
        """Check if the current user has root or sudo privileges.
        
        Returns:
            list: Empty list if the user is not a sudo user, ['sudo'] if the user has sudo privileges.
        """
        if Sudoer.is_root_or_has_sudo():
            return ['sudo']
        else:
            return []

    @staticmethod
    def is_root():
        """Check if the current user is root.
        
        Returns:
            bool: True if the user is root, False otherwise.
        """
        if Sudoer.__is_root__ is None:
            Sudoer.__is_root__ = os.geteuid() == 0
        return Sudoer.__is_root__

    @staticmethod
    def has_sudo():
        """Test if the user can execute a command with sudo.

        Prompts the user for their sudo password if necessary.

        Returns:
            bool: True if the user can use sudo, False otherwise.
        """
        if Sudoer.__is_sudo__ is None:
            try:
                if Sudoer.__handle_signal__ is None:
                    signal.signal(signal.SIGINT, Sudoer.signal_handler)
                    Sudoer.__handle_signal__ = True

                print("The program is trying to use sudo command. It may or may not prompt you to enter password. We don't collect password here. Please verify source code to prevent password leak. If you are not sure, please press Ctl-C to exit.")
                stdout, stderr = Popen(['/bin/sh', '-c', 'sudo true'],
                                     stdin=PIPE, stdout=PIPE, stderr=PIPE,
                                     universal_newlines=True).communicate()
                Sudoer.__is_sudo__ = stderr.strip() == ""
            except (OSError, ValueError):
                Sudoer.__is_sudo__ = False
        return Sudoer.__is_sudo__

    @staticmethod
    def is_root_or_has_sudo():
        """Check if the current user is root or has sudo privileges.
        
        Returns:
            bool: True if the user is root or has sudo privileges, False otherwise.
        """
        if Sudoer.__is_root__ is None:
            Sudoer.__is_root__ = os.geteuid() == 0
        Sudoer.has_sudo()
        return Sudoer.__is_root__ or Sudoer.__is_sudo__ 

    @staticmethod
    def signal_handler(sig, frame):
        if sig == 2:
            print('\nYou pressed Ctrl + c!\n')
        if sig == 3:
            print('\nYou pressed Ctrl + Back Slash!')
        sys.exit()

class ChronicleLogger:
    CLASSNAME = "ChronicleLogger"
    MAJOR_VERSION = 1
    MINOR_VERSION = 0
    PATCH_VERSION = 20 # Updated PATCH_VERSION

    LOG_ARCHIVE_DAYS = 7  # Number of days to keep log files before archiving
    LOG_REMOVAL_DAYS = 30  # Number of days to keep log files before removal

    def __init__(self, logname=b"app", logdir=b"", basedir=b""):
        self.__logname__ = None  # Initialize as None
        self.__basedir__ = None    # Initialize as None
        self.__logdir__ = None    # Initialize as None
        self.__old_logfile_path__ = ctypes.c_char_p(b"")
        self.__is_python__ = None  # Lazy evaluation attribute

        # Set logname and logdir
        if logname=="" or logname==b"":
            # The function requires non empty string for log name
            return
        self.logName(logname)
        if logdir!=b"" and logdir!="":
            self.logDir(logdir)
        else:
            self.logDir("")
        if basedir!=b"" and basedir!="":
            self.baseDir(basedir)
        else:
            self.baseDir("")

        self.__current_logfile_path__ = self._get_log_filename()
        self.ensure_directory_exists(self.__logdir__.decode())

        if self._has_write_permission(self.__current_logfile_path__):
            self.write_to_file(b"\n")

    def strToByte(self, value):
        if isinstance(value, basestring):  # Check if value is a string
            return value.encode()  # Convert str to bytes
        elif value is None or isinstance(value, bytes):
            return value  # Do nothing, return as is
        else:
            raise TypeError("Expected basestring or None or bytes, got {}".format(type(value).__name__))

    def byteToStr(self, value):
        if value is None or isinstance(value, basestring):  # Check if value is a string
            return value  # Do nothing, return as is
        elif isinstance(value, bytes):
            return value.decode()  # Convert str to bytes
        else:
            raise TypeError("Expected basestring or None or bytes, got {}".format(type(value).__name__))

    def inPython(self):
        if self.__is_python__ is None:  # Lazy evaluation
            self.__is_python__ = 'python' in sys.executable
        return self.__is_python__

    def logName(self, logname=None):
        if logname is not None:
            # Convert logname to bytes using strToByte
            self.__logname__ = self.strToByte(logname)

            # Adjust logname if executed by Python
            if self.inPython():
                # Use regex to add hyphens before capital letters and convert to lowercase
                self.__logname__ = re.sub(r'(?<!^)(?=[A-Z])', '-', self.__logname__.decode()).lower().encode()
        else:
            # Getter
            return self.__logname__.decode()

    def __set_base_dir__(self, basedir=b""):
        basedir_str = self.byteToStr(basedir)
        if basedir_str == "":
            # Determine logdir based on user privileges and input
            user_home = os.path.expanduser("~")  # Use string for user home
            if Sudoer.is_root():
                self.__basedir__ = '/var/{}'.format(self.__logname__.decode())
            else:
                self.__basedir__ = os.path.join(user_home, ".app/{}".format(self.__logname__.decode()))
            self.__basedir__ = self.strToByte(self.__basedir__)  # Convert to bytes
        else:
            self.__basedir__ = self.strToByte(basedir)

    def baseDir(self, basedir=None):
        if basedir is not None:
            self.__set_base_dir__(basedir)
        else:
            # Getter
            if self.__logdir__ is None:  # Lazy evaluation
                self.__set_base_dir__()
            return self.__basedir__.decode()

    def __set_log_dir__(self,logname):
        logname_str = self.byteToStr(logname)
        if logname_str == "" :
            # Determine logdir based on user privileges and input
            if Sudoer.is_root():
                self.__logdir__ = '/var/log/{}'.format(self.__logname__.decode())
            else:
                user_home = os.path.expanduser("~")  # Use string for user home
                self.__logdir__ = os.path.join(user_home, ".app/{}".format(self.__logname__.decode()), "log")
            self.__logdir__ = self.strToByte(self.__logdir__)  # Convert to bytes
        else:
            self.__logdir__ = self.strToByte(logname_str)

    def logDir(self, logdir=None):
        if logdir is not None:
            self.__set_log_dir__(logdir)
        else:
            # Getter
            if self.__logdir__ is None:  # Lazy evaluation
                self.__set_log_dir__()
            return self.byteToStr(self.__logdir__)

    def isDebug(self):
        if not hasattr(self, '__is_debug__'):
            self.__is_debug__ = ('DEBUG' in os.environ and os.environ['DEBUG'].lower() == 'show') or \
                                ('debug' in os.environ and os.environ['debug'].lower() == 'show')
        return self.__is_debug__

    @staticmethod
    def class_version():
        return "{} v{}.{}.{}".format(ChronicleLogger.CLASSNAME, ChronicleLogger.MAJOR_VERSION, ChronicleLogger.MINOR_VERSION, ChronicleLogger.PATCH_VERSION)

    def ensure_directory_exists(self, dir_path):
        if dir_path.strip() !='' and not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path)
                print("Created directory: {}".format(dir_path))
            except:
                self.log_message(f"Error making director:{dir_path}", level="ERROR")
    def print_to_console(self, log_entry):
        print(log_entry.decode().strip())

    def print_to_stderr(self, log_entry):
        print(log_entry.decode().strip(), file=sys.stderr)

    def _get_log_filename(self):
        date_str = datetime.now().strftime('%Y%m%d')
        filename = "{}/{}-{}.log".format(self.__logdir__.decode(), self.__logname__.decode(), date_str)
        return ctypes.c_char_p(filename.encode()).value  # Return as cstring

    def log_message(self, message, level=b"INFO", component=b""):
        pid = os.getpid()
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Convert component, message, and level to bytes using strToByte
        component_str = " @{}".format(self.strToByte(component).decode()) if component else ""
        message_str = self.strToByte(message).decode().strip()
        level_str = self.strToByte(level).decode()

        # Construct log_entry as a byte string
        log_entry = "[{}] pid:{} [{}]{} :] {}\n".format(
            self.timestamp, pid, level_str, component_str, message_str
        ).encode()

        new_logfile_path = self._get_log_filename()

        if self.__old_logfile_path__ != new_logfile_path:
            self.log_rotation()
            self.__old_logfile_path__ = new_logfile_path  # Update old_logfile_path
            if self.isDebug():
                log_entry_header = "[{}] pid:{} [{}] @logger :] Using {}\n".format(
                    self.timestamp, pid, level_str, new_logfile_path.decode()
                ).encode()
                log_entry = log_entry_header + log_entry

        if self._has_write_permission(new_logfile_path):
            if level_str.upper in ['ERROR', 'CRITICAL', 'FATAL']:
                self.print_to_stderr(log_entry)
            else:
                self.print_to_console(log_entry)
            self.write_to_file(log_entry)

    def _has_write_permission(self, file_path):
        try:
            with open(file_path, 'a'):
                return True
        except (PermissionError, IOError):
            print("Permission denied for writing to {}".format(file_path), file=sys.stderr)
            return False

    def write_to_file(self, log_entry):
        # Write log entry to file without adding extra new line
        with open(self.__current_logfile_path__, 'a') as log_file:
            log_file.write(log_entry.decode())  # No additional newline here

    def log_rotation(self):
        if not os.path.exists(self.__logdir__.decode()) or not os.listdir(self.__logdir__.decode()):
            print("No log files to rotate in directory: {}".format(self.__logdir__.decode()), file=sys.stderr)
            return
        
        self.archive_old_logs()
        self.remove_old_logs()

    def archive_old_logs(self):
        try:
            for file in os.listdir(self.__logdir__.decode()):
                if file.endswith(".log"):
                    log_date_str = file.split('-')[-1].split('.')[0]
                    log_date = datetime.strptime(log_date_str, '%Y%m%d')
                    if (datetime.now() - log_date).days > self.LOG_ARCHIVE_DAYS:
                        self._archive_log(file.encode())
        except Exception as e:
            print("Error accessing log files for archiving: {}".format(e), file=sys.stderr)

    def _archive_log(self, log_filename):
        log_file_path = os.path.join(self.__logdir__.decode(), log_filename.decode())
        archive_name = log_filename.replace(b'.log', b'.tar.gz')
        archive_path = os.path.join(self.__logdir__.decode(), archive_name.decode())

        try:
            with tarfile.open(archive_path, "w:gz") as tar:
                tar.add(log_file_path, arcname=log_filename.decode())
            os.remove(log_file_path)  # Remove the original log file after archiving
            print("Archived log file: {}".format(archive_path))
        except Exception as e:
            print("Error archiving log file {}: {}".format(log_filename.decode(), e), file=sys.stderr)

    def remove_old_logs(self):
        try:
            for file in os.listdir(self.__logdir__.decode()):
                if file.endswith(".log"):
                    log_date_str = file.split('-')[-1].split('.')[0]
                    log_date = datetime.strptime(log_date_str, '%Y%m%d')
                    if (datetime.now() - log_date).days > self.LOG_REMOVAL_DAYS:
                        os.remove(os.path.join(self.__logdir__.decode(), file))
                        print("Removed old log file: {}".format(file.decode()))
        except Exception as e:
            print("Error accessing log files for removal: {}".format(e), file=sys.stderr)

class Example:
    # Remember to replace Example to name of the class
    CLASSNAME = "Example"
    MAJOR_VERSION = 1
    MINOR_VERSION = 0
    PATCH_VERSION = 1

    def __init__(self, basedir="/var/app",  logger=None):
        """
        Initializes the PyxPy object with source and target folder paths and sets up the logger.
        """
        self.basedir = basedir
        self.logger = logger

    @staticmethod
    def class_version():
        return f"{Example.CLASSNAME} v{Example.MAJOR_VERSION}.{Example.MINOR_VERSION}.{Example.PATCH_VERSION}"

    def log(self, message, level="INFO", component=""):
        """Logs a message using the provided logger if available."""
        if self.logger:
            self.logger.log_message(message, level, component)
        else:
            print(message)  # Fallback to print if no logger is provided

    def info(self):
        print("This is an example app")

def usage(appname):
    print(f"Usage: {appname} info")

def main():
    appname = 'LoggedExample'
    MAJOR_VERSION = 0
    MINOR_VERSION = 1
    PATCH_VERSION = 0

    # Create logger instance
    logger = ChronicleLogger(logname=appname)
    appname=logger.logName()    
    basedir=logger.baseDir()
    if logger.isDebug():
        logger.log_message(f"{appname} v{MAJOR_VERSION}.{MINOR_VERSION}.{PATCH_VERSION} ({__file__}) with the following:", component="main")
        logger.log_message(f">> {ChronicleLogger.class_version()}", component="main")
        logger.log_message(f">> {Sudoer.class_version()}", component="main")

    if len(sys.argv) < 2:
        usage(appname)
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd=="info":
        app = Example(basedir=basedir, logger=logger)
        app.info()
    else:
        usage(appname)
        sys.exit(1)

if __name__ == '__main__':
    main()
