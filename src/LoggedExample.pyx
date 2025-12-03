#!/usr/bin/env python3
try:
    get_ipython
    getIpythonExists = True
except:
    getIpythonExists = False
    get_ipython = {}
import os
import re
import sys
try: 
    __file__
except NameError: 
    __file__ = ''
def resolveSysPath():
    this = re.compile(r"/\./").sub("/", __file__)
    if this == "built-in" or this == "":
        if getIpythonExists:
            try:
                shell = get_ipython().__class__.__name__
            except NameError:
                pass
        exec = ""
        if "_" in os.environ:
            exec = os.environ["_"]
            if exec.startswith(("/usr/local/bin", "/usr/bin", os.getcwd(), "/home/")):
                exec = os.environ["_"]
            else:
                exec = ""
        elif "SUDO_COMMAND" in os.environ: 
            exec = os.environ["SUDO_COMMAND"]
        if exec:
            if exec.startswith('/'):
                this = exec
            else:
                pwd = os.getcwd()
                this = os.path.join(pwd, exec)
            current_dir = os.path.dirname(os.path.abspath(this))
            if current_dir not in sys.path:
                sys.path.insert(0, current_dir)
        else:
            if "/usr/bin" not in sys.path:
                sys.path.insert(0, "/usr/bin")
            if "/usr/local/bin" not in sys.path:
                sys.path.insert(0, "/usr/local/bin")
        if "'/usr/lib/python3/dist-packages'" not in sys.path:
            sys.path.append('/usr/lib/python3/dist-packages')
        version=""
        for pack in sys.path:
            if "/usr/lib/python3." in pack:
                version = pack.split(".")[1]
        if version != "":
            dist = f"/usr/local/lib/python3.{version}/dist-packages"
            if dist not in sys.path:
                sys.path.append(dist)
        if '' not in sys.path:
            sys.path.insert(0,'')
    return this
# Run resolveSysPath() before any import statement which looks for *.so at the same folder 
# no matter this program is run using absolution of relative path
# If you need to compile this program in cython binary, you need to use this.
__file__ = resolveSysPath()

# The following are cythonized *.so libraries stored in the same folder
from ChronicleLogger import ChronicleLogger
from Sudoer import Sudoer
import signal
import shutil

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
    appname = 'Example'
    MAJOR_VERSION = 1
    MINOR_VERSION = 0
    PATCH_VERSION = 5

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

if __name__ == '__main__':
    main()
