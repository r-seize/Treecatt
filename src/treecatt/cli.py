"""
Command-line interface for TreeCatt
"""

import os
import sys
import argparse


def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description         = 'TreeCatt - Display directory tree and file contents',
        formatter_class     = argparse.RawDescriptionHelpFormatter,
        epilog              = """
USAGE EXAMPLES — COMPLETE REFERENCE
==================================

BASIC USAGE
-----------
  treecatt
      Run full analysis on the current directory with default settings.

  treecatt /var/www
      Run full analysis on a specific path.


TREE DISPLAY MODES
------------------
  treecatt --tree
      Display only the directory tree (no file contents).

  treecatt --tree --depth 3
      Display the tree up to a maximum depth of 3 levels.

  treecatt --tree --tree-size
      Display file sizes next to each file in the tree.

  treecatt --tree --permissions
      Display Unix permissions in the tree output.

  treecatt --tree --dates
      Display last modification dates in the tree.

  treecatt --tree --git-status
      Display Git status (modified, untracked, ignored) in the tree.

  treecatt --tree --tree-size --permissions --dates --git-status
      Full detailed tree view with all available metadata.


FILTERING FILES
---------------
  treecatt --ignore "*.log" "*.tmp" "__pycache__"
      Ignore additional file or directory patterns.

  treecatt --no-default-ignore
      Disable built-in ignore rules (e.g. .git, node_modules).

  treecatt --include "*.py" "*.md"
      Include only files matching these patterns.

  treecatt --filter-date 24h
      Show only files modified in the last 24 hours.

  treecatt --filter-date 7d
      Show only files modified in the last 7 days.

  treecatt --max-size 1MB
      Exclude files larger than the specified size.

  treecatt --max-size 500KB
      Exclude files larger than 500 KB.


FILE CONTENT DISPLAY
--------------------
  treecatt --view .env config.yaml secrets.json
      Force display of sensitive or normally hidden files.

  treecatt --line-numbers
      Display line numbers when showing file contents.


ANALYSIS FEATURES
-----------------
  treecatt --checksums md5
      Calculate MD5 checksums for all files.

  treecatt --checksums sha256
      Calculate SHA-256 checksums for all files.

  treecatt --checksums sha256 --duplicates
      Detect duplicate files using cryptographic hashes.


SEARCH
------
  treecatt --search "TODO"
      Search for a text pattern inside all analyzed files.

  treecatt --search "password"
      Search for potentially sensitive keywords.


SORTING
-------
  treecatt --sort name
      Sort files alphabetically (default).

  treecatt --sort size
      Sort files by size.

  treecatt --sort date
      Sort files by modification date.

  treecatt --sort ext
      Sort files by file extension.


COMBINED REAL-WORLD EXAMPLES
----------------------------
  treecatt --tree --depth 4 --include "*.py" --sort size
      Show a Python project tree, limited to 4 levels, sorted by file size.

  treecatt --search "FIXME" --filter-date 2w
      Search for recent FIXME comments from the last 2 weeks.

  treecatt --checksums sha1 --duplicates --max-size 5MB
      Find duplicate files smaller than 5 MB using SHA-1 hashes.

  treecatt --tree --git-status --ignore node_modules dist
      Show project tree with Git status while ignoring build artifacts.

  treecatt --view .env --line-numbers --search "API_KEY"
      Inspect environment files and search for API keys.


MISC
----
  treecatt --version
      Display TreeCatt version information.
        """
    )

    parser.add_argument('path', nargs='?', default=os.getcwd(), 
                       help='Path to analyze (default: current directory)')

    parser.add_argument('--ignore', '-i', nargs='+', metavar='PATTERN',
                       help='Additional patterns to ignore (e.g., "*.log" "temp")')

    parser.add_argument('--view', '-v', nargs='+', metavar='FILE',
                       help='Sensitive files to display (e.g., .env secrets.json)')

    parser.add_argument('--tree', '-t', action='store_true',
                       help='Display only tree structure (no file contents)')

    parser.add_argument('--tree-size', action='store_true',
                       help='Show file sizes in tree view')

    parser.add_argument('--line-numbers', '-n', action='store_true',
                       help='Display line numbers in file contents')

    parser.add_argument('--git-status', '-g', action='store_true',
                       help='Show git status indicators ([M], [A], [?], etc.)')

    parser.add_argument('--permissions', '-p', action='store_true',
                       help='Show Unix permissions (e.g., rwxr-xr-x)')

    parser.add_argument('--dates', action='store_true',
                       help='Show modification dates and times')

    parser.add_argument('--checksums', choices=['md5', 'sha1', 'sha256'],
                       help='Calculate file checksums using specified algorithm')

    parser.add_argument('--duplicates', action='store_true',
                       help='Detect and report duplicate files (implies --checksums md5)')

    parser.add_argument('--search', metavar='PATTERN',
                       help='Search for text pattern in file contents')

    parser.add_argument('--filter-date', metavar='TIME',
                       help='Filter files by modification time (e.g., 7d, 24h, 2w)')

    parser.add_argument('--sort', choices=['name', 'size', 'date', 'ext'], default='name',
                       help='Sort files by: name (default), size, date, or extension')

    parser.add_argument('--max-size', '-s', default='1MB',
                       help='Maximum file size to display (default: 1MB, e.g., 500KB, 5MB)')

    parser.add_argument('--depth', '-d', type=int,
                       help='Maximum tree depth to display')

    parser.add_argument('--include', nargs='+', metavar='PATTERN',
                       help='Include only files matching these patterns (e.g., "*.py" "*.js")')

    parser.add_argument('--no-default-ignore', action='store_true',
                       help='Disable default ignore rules (.git, node_modules, etc.)')

    parser.add_argument('--version', action='version', version='%(prog)s 0.1.4')

    return parser


def parse_size(size_str: str) -> int:
    """Parse size string and convert to bytes
    
    Args:
        size_str: Size string (e.g., '1MB', '500KB', '2GB')
    
    Returns:
        Size in bytes
    
    Raises:
        SystemExit: If size string is invalid
    """
    size_str_upper = size_str.upper()
    multiplier = 1
    
    if size_str_upper.endswith('KB'):
        multiplier = 1024
        size_str_upper = size_str_upper[:-2]
    elif size_str_upper.endswith('MB'):
        multiplier = 1024 * 1024
        size_str_upper = size_str_upper[:-2]
    elif size_str_upper.endswith('GB'):
        multiplier = 1024 * 1024 * 1024
        size_str_upper = size_str_upper[:-2]

    try:
        return int(float(size_str_upper) * multiplier)
    except ValueError:
        print(f"Error: Invalid size format '{size_str}'. Use format like: 1MB, 500KB, 2GB", 
              file=sys.stderr)
        sys.exit(1)