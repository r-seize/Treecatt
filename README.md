<div align="center">

```
    ███        ▄████████    ▄████████    ▄████████  ▄████████    ▄████████     ███         ███     
▀█████████▄   ███    ███   ███    ███   ███    ███ ███    ███   ███    ███ ▀█████████▄ ▀█████████▄ 
   ▀███▀▀██   ███    ███   ███    █▀    ███    █▀  ███    █▀    ███    ███    ▀███▀▀██    ▀███▀▀██ 
    ███   ▀  ▄███▄▄▄▄██▀  ▄███▄▄▄      ▄███▄▄▄     ███          ███    ███     ███   ▀     ███   ▀ 
    ███     ▀▀███▀▀▀▀▀   ▀▀███▀▀▀     ▀▀███▀▀▀     ███        ▀███████████     ███         ███     
    ███     ▀███████████   ███    █▄    ███    █▄  ███    █▄    ███    ███     ███         ███     
    ███       ███    ███   ███    ███   ███    ███ ███    ███   ███    ███     ███         ███     
   ▄████▀     ███    ███   ██████████   ██████████ ████████▀    ███    █▀     ▄████▀      ▄████▀   
              ███    ███                                                                           
```

**Advanced CLI tool combining tree and cat functionality**

[![Version](https://img.shields.io/badge/version-0.1.1-blue.svg)](https://github.com/r-seize/TreeCatt/releases)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-GPL-orange.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey.svg)]()

</div>

## TreeCatt

TreeCatt is a versatile command-line tool to analyze directories and display file contents efficiently. It combines tree visualization, metadata display, content search, checksum calculations, and git integration into a single, easy-to-use interface.

## Installation

### 1. Using the install script (Linux/macOS/Windows)

```bash
curl -sSL https://raw.githubusercontent.com/r-seize/TreeCatt/main/install.sh | bash
```

> If your system Python is managed by the OS (externally-managed environment), use a virtual environment or pipx:

```bash
python3 -m venv ~/treecatt-venv
source ~/treecatt-venv/bin/activate
pip install https://github.com/r-seize/TreeCatt/releases/download/v0.1.1/treecatt-0.1.1-py3-none-any.whl
```

### 2. Using pip directly from the release archive

```bash
pip3 install https://github.com/r-seize/TreeCatt/releases/download/v0.1.1/treecatt-0.1.1-py3-none-any.whl
```

### 3. On Ubuntu/Debian using the .deb package

```bash
wget https://github.com/r-seize/TreeCatt/releases/download/v0.1.1/treecatt_0.1.1_all.deb
sudo dpkg -i treecatt_0.1.1_all.deb
```

## Usage

### Basic Usage

| Command | Description |
|---------|-------------|
| `treecatt` | Run a full analysis on the current directory with default settings. |
| `treecatt /path/to/directory` | Run a full analysis on the specified path. |

### Tree Display

| Command | Description |
|---------|-------------|
| `treecatt --tree` | Display only the directory tree (no file contents). |
| `treecatt --tree --depth 3` | Limit the tree display to 3 levels deep. |
| `treecatt --tree --tree-size` | Show file sizes in the tree output. |
| `treecatt --tree --permissions` | Show Unix file permissions in the tree. |
| `treecatt --tree --dates` | Show file modification dates in the tree. |
| `treecatt --tree --git-status` | Show Git status (modified, untracked, ignored) in the tree. |
| `treecatt --tree --tree-size --permissions --dates --git-status` | Display a fully detailed tree with all available metadata. |

### Filtering Files

| Command | Description |
|---------|-------------|
| `treecatt --ignore "*.log" "*.tmp" "__pycache__"` | Ignore additional file or directory patterns. |
| `treecatt --no-default-ignore` | Disable built-in ignore rules (e.g., `.git`, `node_modules`). |
| `treecatt --include "*.py" "*.md"` | Include only files matching specific patterns. |
| `treecatt --filter-date 7d` | Show only files modified in the last 7 days. |
| `treecatt --max-size 1MB` | Exclude files larger than the specified size. |

### File Content Display

| Command | Description |
|---------|-------------|
| `treecatt --view .env config.yaml` | Force display of sensitive or normally hidden files. |
| `treecatt --line-numbers` | Display line numbers when showing file contents. |

### Analysis Features

| Command | Description |
|---------|-------------|
| `treecatt --checksums md5` | Calculate MD5 checksums for all files. |
| `treecatt --checksums sha1` | Calculate SHA-1 checksums for all files. |
| `treecatt --checksums sha256` | Calculate SHA-256 checksums for all files. |
| `treecatt --checksums sha256 --duplicates` | Detect duplicate files using cryptographic hashes. |

### Search

| Command | Description |
|---------|-------------|
| `treecatt --search "TODO"` | Search for a text pattern in all analyzed files. |
| `treecatt --search "password"` | Search for potentially sensitive keywords. |

### Sorting

| Command | Description |
|---------|-------------|
| `treecatt --sort name` | Sort files alphabetically (default). |
| `treecatt --sort size` | Sort files by size. |
| `treecatt --sort date` | Sort files by modification date. |
| `treecatt --sort ext` | Sort files by file extension. |

### Combined Examples

| Command | Description |
|---------|-------------|
| `treecatt --tree --depth 4 --include "*.py" --sort size` | Analyze a Python project tree, limited to 4 levels, sorted by file size. |
| `treecatt --search "FIXME" --filter-date 2w` | Search for recent "FIXME" comments from the last two weeks. |
| `treecatt --checksums sha1 --duplicates --max-size 5MB` | Find duplicate files smaller than 5 MB using SHA-1 hashes. |
| `treecatt --tree --git-status --ignore node_modules dist` | Show project tree while ignoring build artifacts. |
| `treecatt --view .env --line-numbers --search "API_KEY"` | Inspect environment files and search for API keys. |

### Miscellaneous

| Command | Description |
|---------|-------------|
| `treecatt --version` | Display TreeCatt version information. |

## Uninstallation

### Linux/macOS

* If installed via `.deb`:

```bash
sudo dpkg -r treecatt
sudo apt-get autoremove
```

* If installed via `pip`:

```bash
pip3 uninstall treecatt
```

* If installed in a virtual environment:

```bash
rm -rf /path/to/treecatt-venv
```

### Windows

* If installed via `pip` or in a virtual environment:

```bash
pip uninstall treecatt
rm -rf C:\path\to\treecatt-venv
```

## Contributing

We welcome contributions, bug reports, and feature requests. Please open an issue or submit a pull request on [GitHub](https://github.com/r-seize/TreeCatt).

---

## License

TreeCatt is released under the [GPL License](LICENSE).

## Links

* [GitHub Repository](https://github.com/r-seize/TreeCatt)
* [Release v0.1.1](https://github.com/r-seize/TreeCatt/releases/tag/v0.1.1)

## About

We’d like to thank everyone who contributed ideas, tested the tool, or provided feedback during development. Your support is greatly appreciated!

If you have suggestions, feature requests, or improvements, please don’t hesitate to open an issue or submit a pull request. Every contribution helps make FileGen better for everyone.
