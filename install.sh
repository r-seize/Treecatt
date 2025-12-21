#!/bin/bash
set -e

VERSION="0.1.0"
PACKAGE_NAME="treecatt"
INSTALL_DIR="/usr/local"

echo "🌳 Installing TreeCatt v${VERSION}"
echo ""

if [ "$EUID" -ne 0 ] && [ ! -w "$INSTALL_DIR/bin" ]; then 
    echo "❌ This script requires root permissions."
    echo "   Run with: sudo ./install.sh"
    exit 1
fi

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    OS="windows"
else
    OS="unknown"
fi

echo "📦 Detected system: $OS"

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed."
    echo "   Install Python 3.8+ and try again."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Python $PYTHON_VERSION detected"

if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed."
    echo "   Install pip and try again."
    exit 1
fi

echo ""
echo "🔧 Installing..."

pip3 install .

echo ""
echo "✅ Installation successful!"
echo ""
echo "To get started, try:"
echo "  $ treecatt --help"
echo "  $ treecatt ."
echo ""
echo "Full documentation: https://github.com/yourusername/treecatt"