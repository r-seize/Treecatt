<div align="center">

```
████████╗██████╗ ███████╗███████╗ ██████╗ █████╗ ████████╗████████╗
╚══██╔══╝██╔══██╗██╔════╝██╔════╝██╔════╝██╔══██╗╚══██╔══╝╚══██╔══╝
   ██║   ██████╔╝█████╗  █████╗  ██║     ███████║   ██║      ██║   
   ██║   ██╔══██╗██╔══╝  ██╔══╝  ██║     ██╔══██║   ██║      ██║   
   ██║   ██║  ██║███████╗███████╗╚██████╗██║  ██║   ██║      ██║   
   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝   ╚═╝      ╚═╝   
```

**Advanced CLI tool combining tree and cat functionality**

[![Version](https://img.shields.io/badge/version-0.2.1-blue.svg)](https://github.com/r-seize/TreeCatt/releases)
[![Python](https://img.shields.io/badge/python-3.12+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-BSD--3--Clause-orange.svg)](LICENSE)
[![Maintained](https://img.shields.io/badge/maintained-yes-brightgreen.svg)](https://github.com/r-seize/TreeCatt)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey.svg)]()

</div>

## TreeCatt

TreeCatt is a versatile command-line tool to analyze directories and display file contents efficiently. It combines tree visualization, metadata display, and git integration into a single, easy-to-use interface.

## Installation

### Method 1: pipx (Recommended)

```bash
# Install pipx if needed
sudo apt install pipx  # Ubuntu/Debian
# or: brew install pipx (macOS)

pipx ensurepath
pipx install git+https://github.com/r-seize/TreeCatt.git@v0.2.1
```

### Method 2: Ubuntu/Debian (.deb)

```bash
wget https://github.com/r-seize/TreeCatt/releases/download/v0.2.1/python3-treecatt_0.2.1-1_all.deb
sudo dpkg -i python3-treecatt_0.2.1-1_all.deb
```

### Method 3: Virtual Environment

```bash
python3 -m venv ~/.treecatt-venv
source ~/.treecatt-venv/bin/activate
pip install git+https://github.com/r-seize/TreeCatt.git@v0.2.1

# Add to PATH (Linux/macOS)
ln -s ~/.treecatt-venv/bin/treecatt ~/.local/bin/treecatt
```

### Verification

After installation, verify it works:

```bash
treecatt --version
treecatt --help
```

## Usage

### Basic Usage

| Command | Description |
|---------|-------------|
| `treecatt` | Analyze the current directory. |
| `treecatt /path/to/directory` | Analyze a specific path. |

### Tree Display

| Command | Description |
|---------|-------------|
| `treecatt --tree` | Display only the directory tree. |
| `treecatt --tree --depth 3` | Limit the tree display to 3 levels deep. |
| `treecatt --tree --tree-size` | Show file sizes in the tree output. |
| `treecatt --tree --permissions` | Show Unix file permissions in the tree. |
| `treecatt --tree --dates` | Show file modification dates in the tree. |
| `treecatt --tree --git-status` | Show Git status (`[M]` modified, `[A]` added, `[?]` untracked…) in the tree. |
| `treecatt --tree --tree-size --permissions --dates --git-status` | Display a fully detailed tree with all available metadata. |

### Sorting

| Command | Description |
|---------|-------------|
| `treecatt --sort name` | Sort files alphabetically (default). |
| `treecatt --sort size` | Sort files by size (largest first). |
| `treecatt --sort date` | Sort files by modification date (newest first). |
| `treecatt --sort ext` | Sort files by file extension. |

### Combined Examples

| Command | Description |
|---------|-------------|
| `treecatt --tree --depth 2 --sort size` | Tree limited to 2 levels, sorted by size. |
| `treecatt --tree --git-status --sort date` | Tree with Git status, sorted by date. |
| `treecatt --tree --tree-size --permissions --dates --depth 3` | Full metadata tree, 3 levels deep. |

### Miscellaneous

| Command | Description |
|---------|-------------|
| `treecatt --version` | Display TreeCatt version. |
| `treecatt --help` | Show all available options. |

## Uninstallation

### Linux/macOS

* If installed via pipx:

```bash
pipx uninstall treecatt
```

* If installed via `.deb`:

```bash
sudo dpkg -r treecatt
sudo apt-get autoremove
```

* If installed in a virtual environment:

```bash
rm -rf ~/.treecatt-venv
```

### Windows

* If installed via pipx:

```bash
pipx uninstall treecatt
```

* If installed via pip or virtual environment:

```bash
pip uninstall treecatt
rm -rf C:\path\to\treecatt-venv
```

## Contributing

We welcome contributions, bug reports, and feature requests. Please open an issue or submit a pull request on [GitHub](https://github.com/r-seize/TreeCatt).

---

## License

TreeCatt is released under the [BSD 3-Clause License](LICENSE).

## Links

* [GitHub Repository](https://github.com/r-seize/TreeCatt)
* [Release v0.2.1](https://github.com/r-seize/TreeCatt/releases/tag/v0.2.1)

## About

We'd like to thank everyone who contributed ideas, tested the tool, or provided feedback during development. Your support is greatly appreciated!

If you have suggestions, feature requests, or improvements, please don’t hesitate to open an issue or submit a pull request. Every contribution helps make TreeCatt better for everyone.
