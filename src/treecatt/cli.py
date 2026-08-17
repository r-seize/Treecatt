"""
Command-line interface for TreeCatt
"""

import os
import argparse


def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description='TreeCatt - Display directory tree',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES
--------
  treecatt                          Analyze current directory
  treecatt /path/to/dir             Analyze a specific path
  treecatt --tree                   Tree only (no file contents)
  treecatt --tree --depth 3         Limit depth to 3 levels
  treecatt --tree --tree-size       Show file sizes
  treecatt --tree --permissions     Show Unix permissions
  treecatt --tree --dates           Show modification dates
  treecatt --tree --git-status      Show Git status
  treecatt --sort size              Sort by size
  treecatt --sort date              Sort by date
  treecatt --sort ext               Sort by extension
        """
    )

    parser.add_argument(
        'path', nargs='?', default=os.getcwd(),
        help='Path to analyze (default: current directory)'
    )
    parser.add_argument(
        '--tree', '-t', action='store_true',
        help='Display only the tree (no file contents)'
    )
    parser.add_argument(
        '--tree-size', action='store_true',
        help='Show file sizes in tree'
    )
    parser.add_argument(
        '--permissions', '-p', action='store_true',
        help='Show Unix permissions'
    )
    parser.add_argument(
        '--dates', action='store_true',
        help='Show modification dates'
    )
    parser.add_argument(
        '--git-status', '-g', action='store_true',
        help='Show Git status indicators'
    )
    parser.add_argument(
        '--sort', choices=['name', 'size', 'date', 'ext'], default='name',
        help='Sort by: name (default), size, date, ext'
    )
    parser.add_argument(
        '--depth', '-d', type=int, default=None,
        help='Maximum tree depth'
    )
    parser.add_argument(
        '--version', action='version', version='%(prog)s 0.2.1'
    )

    return parser