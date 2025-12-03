# Design Document for `logged-example`

## Overview
The `logged-example` module provides a utility for converting Cython project folder structures from camelCase to lowercase snake_case. It processes a source folder containing subfolders with Cython projects, transforms the project names, and organizes the files into a specified target folder. The module integrates the `ChronicleLogger` class for robust and reliable logging throughout the conversion process. Most of the imported libraries are in `.so` format and are stored in the same directory as the executable Python script.

## The folder structure for the project: Loggedlogged-example
 * Project: LoggedExample is a Cython (CyMaster type) project!
    ```
    LoggedExample/
    ├── README.md
    ├── build/
    │   ├── bdist.linux-x86_64/
    │   └── lib/
    │       ├── logged_example/
    │       │   ├── __init__.py
    │       │   ├── __main__.py
    │       │   └── cli.py
    │       └── setup.py
    ├── build.sh
    ├── cy-master
    ├── cy-master.ini
    ├── docs/
    │   ├── CHANGELOG.md
    │   ├── LoggedExample-spec.md
    │   └── folder-structure.md
    ├── pyproject.toml
    └── src/
        ├── LoggedExample.pyx
        ├── logged_example/
        │   ├── __init__.py
        │   ├── __main__.py
        │   └── cli.py
        └── setup.py
    ```

### cy-master.ini
 * The cy-master.ini file serves as the primary configuration file for CyMaster-type Cython projects:
    ```
    [project]
    srcFolder = src
    buildFolder = build
    targetName = LoggedExample
    targetType = bin
    ```
## Target Operating System
- **Linux**: The module is specifically designed for Linux environments and utilizes Linux-specific features for file handling and permissions.

## Purpose of `resolveSysPath`
The `resolveSysPath` function is essential for dynamically adjusting the Python path based on the execution context. It resolves the path of the current script and adds it to `sys.path`, enabling the import of shared libraries (e.g., Cython-generated `.so` files) located in the same directory. This functionality is particularly important in non-standard environments, such as pipelines or Jupyter notebooks.

## Folder Structure
- **Source Folder**: Contains subfolders for each Cython project, with a `src` directory housing `*.pyx` files and a `cy-master.ini` file.
- **Target Folder**: The destination for transformed project folders.

## Common Folders
- **Source Folder**: The user-defined root folder containing Cython projects.
- **Target Folder**: The user-defined destination for the converted projects.

## Specifications of `cy-master.ini`
The `cy-master.ini` file contains configuration settings for the Cython project, structured as follows:
```ini
[project]
srcFolder = src
buildFolder = build
targetName = LoggedExample
targetType = bin
require = ChronicleLogger, Sudoer
```

### Parameters
- **info**: Displays an logged-example message.

## Project Name Conversion Rules
1. **CamelCase to Snake_case**: Convert project names from camelCase to lowercase snake_case using underscores.
2. **Directory Creation**: Create a directory in the target folder with the lowercase snake_case project name if it does not already exist.
3. **File Handling**: 
   - Create a `src` subfolder within the new lowercase snake_case project folder.
   - Copy all `*.pyx` files from the original `src` folder, renaming them to `*.py`.
   - Copy the `cy-master.ini` file to the new project folder.

## Class Structure

### Attributes
| Variable Name       | Description                                               |
|---------------------|-----------------------------------------------------------|
| `logger`            | Instance of `ChronicleLogger` for logging operations.    |
| `project_name`      | Name of the project in camelCase format.                 |

### Methods

#### Instance Methods

- **`__init__(self, source_folder, target_folder)`**
  - **Logic**: Initializes the `logged-example` object with source and target folder paths and sets up the logger.
  - **Input Parameters**:
    - `source_folder` (str): The path to the source folder.
    - `target_folder` (str): The path to the target folder.
  - **Return Parameters**: None.

## Functionality Supported
The `logged-example` module supports the following functionalities:
- Log operations and errors using the `ChronicleLogger` for effective debugging and monitoring.
- Display an logged-example message.

## Usage logged-example
```python
from chroniclelogger import ChronicleLogger
from logged-example import logged-example

# Create a logger instance
logger = ChronicleLogger(logname="logged-example")

# Create an instance of the logged-example class
app = logged-example(source_folder="/path/to/source", target_folder="/path/to/target")

# Display an logged-example message
app.info()
logger.log_message("Operation completed successfully", level="INFO")
```

## Conclusion
The `logged-example` module serves as a template for well-structured Python projects, targeting compilation into Linux binary files. 

### Future Considerations
- Ensure that any modifications to critical functions like `resolveSysPath()` maintain the original logic to avoid bugs.
- Implement unit tests for key functionalities, especially for path resolution and project conversion, to verify behavior across various environments.