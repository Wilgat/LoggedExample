# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),  
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.1] - 2025-12-25

### Added
- Enhanced debug output in `DEBUG=show` mode: now displays a complete dump of ChronicleLogger state + all relevant environment variables (`sys.executable`, `VIRTUAL_ENV`, `CONDA_*`, `PYENV_*`, etc.)
- New section in README.md: comprehensive **Environment Guide** with purpose, installation steps, and typical log locations for:
  - venv
  - pyenv
  - pyenv + virtualenv plugin
  - Miniconda
  - Anaconda
  - root vs non-root usage
- Early prominent description of ChronicleLogger with direct PyPI link in README.md
- Consistent use of recommended two-digit pyenv version notation (`3.12`) throughout documentation

### Changed
- Updated version to 1.1.1
- Improved README.md structure and clarity for better user onboarding across different Python environment workflows
- Minor refinements to debug output formatting (better alignment, separators)

### Fixed
- Small documentation inconsistencies regarding pyenv version notation

## [1.1.0] - 2025-12-15

### Added
- Full environment detection support in ChronicleLogger (used by LoggedExample):
  - venv (`inVenv()`, `venv_path()`)
  - pyenv (`inPyenv()`, `pyenvVenv()`)
  - Conda/Miniconda/Anaconda (`inConda()`, `condaPath()`)
- Automatic log placement inside active environment directories (e.g. `<env>/.app/logged-example/log/`)
- Privilege-aware path selection preserved across environments
- Updated debug mode to show environment detection results

### Changed
- Bumped version to 1.1.0
- Improved README.md with environment comparison table

## [1.0.0] - 2025-12-10

### Added
- Initial stable release (v1.0.0)
- Console entrypoint `logged-example`
- Basic `info` command
- Integration with ChronicleLogger v1.1.0
- Full cross-version compatibility (Python 2.7 & 3.x)

### Changed
- Finalized project structure, packaging, and documentation

## [0.1.0] - 2025-12-03

### Added
- Initial public release of `logged-example`
- Full-featured logging system via `ChronicleLogger` with:
  - Daily log rotation (YYYYMMDD-based filenames)
  - Automatic archiving of logs older than 7 days (`.tar.gz`)
  - Automatic removal of logs older than 30 days
  - Smart log directory selection:
    - `/var/log/<appname>` when running as root
    - `~/.app/<appname>/log` for regular users
- `Sudoer` utility class with safe sudo detection and user warning
- Console script entrypoint: `logged-example`
  - Run `logged-example info` to display basic application info
- Comprehensive cross-Python compatibility:
  - Python 2.7 and Python 3.5–3.14 supported
  - Tested on Linux and macOS
- MIT-licensed open source project
- Complete packaging setup using `pyproject.toml` + `setuptools`
- POSIX-compliant build script (`build.sh`) with commands:
  - `setup`, `clean`, `build`, `upload`, `test`, `release`, `tag`, `git`
- Editable/development install support (`pip install -e .`)

### Security
- `Sudoer.has_sudo()` displays a clear warning before prompting for password
- No password collection or logging — designed to be audit-safe

### Documentation
- `README.md` with installation and usage instructions
- Design specification: `docs/LoggedExample-spec.md`
- This `CHANGELOG.md`

This is the foundational release intended as a robust, production-ready logging template that can be dropped into any Python project (including Cython-based ones).