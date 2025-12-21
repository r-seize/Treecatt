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
Voici un README adapté à ton projet **TreeCatt**, en s’inspirant du style de ton exemple FileGen et du code que tu m’as fourni :

**Advanced CLI tool combining tree and cat functionality**

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/r-seize/TreeCatt/releases)
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
pip install https://github.com/r-seize/TreeCatt/releases/download/v0.1.0/treecatt-0.1.0-py3-none-any.whl
```

### 2. Using pip directly from the release archive

```bash
pip3 install https://github.com/r-seize/TreeCatt/releases/download/v0.1.0/treecatt-0.1.0-py3-none-any.whl
```

### 3. On Ubuntu/Debian using the .deb package

```bash
wget https://github.com/r-seize/TreeCatt/releases/download/v0.1.0/treecatt_0.1.0_all.deb
sudo dpkg -i treecatt_0.1.0_all.deb
```

## Usage

```bash
treecatt .                                    # Full analysis
treecatt . --tree                             # Tree only
treecatt . --tree --tree-size                 # Tree with file sizes
treecatt . --tree --permissions               # Tree with permissions
treecatt . --tree --dates                     # Tree with modification dates
treecatt . --tree --git-status                # Show git status
treecatt . --checksums md5 --duplicates       # Find duplicate files
treecatt . --search "TODO"                    # Search in files
treecatt . --filter-date 7d                   # Filter recent files
treecatt . --sort size                        # Sort by size
```

## Features

| Feature                                             | Status |
| --------------------------------------------------- | ------ |
| Directory tree display                              | ✅ Done |
| File content display                                | ✅ Done |
| Git status integration                              | ✅ Done |
| Unix permissions display                            | ✅ Done |
| Duplicate file detection                            | ✅ Done |
| Content search                                      | ✅ Done |
| Date filtering                                      | ✅ Done |
| Multiple sort options (name, size, date, extension) | ✅ Done |
| Checksum calculation (MD5, SHA1, SHA256)            | ✅ Done |

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
* [Release v0.1.0](https://github.com/r-seize/TreeCatt/releases/tag/v0.1.0)

## About

We’d like to thank everyone who contributed ideas, tested the tool, or provided feedback during development. Your support is greatly appreciated!

If you have suggestions, feature requests, or improvements, please don’t hesitate to open an issue or submit a pull request. Every contribution helps make FileGen better for everyone.