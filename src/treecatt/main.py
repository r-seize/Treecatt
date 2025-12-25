#!/usr/bin/env python3
"""
TreeCatt - Main module
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Optional

from treecatt.constants import DEFAULT_IGNORE, SENSITIVE_FILES
from treecatt.features import (
    GitStatusManager, ChecksumManager,
    format_size, get_permissions, get_file_dates, matches_date_filter,
    read_file_content, should_ignore, search_in_file, sort_entries
)

VERSION = "0.1.1"


class TreeCatt:
    """Main TreeCatt class for tree generation and file display"""
    
    def __init__(self, 
                 root_path: str,
                 ignore_patterns: Optional[List[str]]   = None,
                 view_sensitive: Optional[List[str]]    = None,
                 max_file_size: int                     = 1024 * 1024,
                 show_tree: bool                        = False,
                 show_tree_size: bool                   = False,
                 show_line_numbers: bool                = False,
                 show_git_status: bool                  = False,
                 show_permissions: bool                 = False,
                 show_dates: bool                       = False,
                 show_checksums: bool                   = False,
                 checksum_type: str                     = 'md5',
                 filter_by_date: Optional[str]          = None,
                 search_content: Optional[str]          = None,
                 show_duplicates: bool                  = False,
                 sort_by: str                           = 'name',
                 max_depth: Optional[int]               = None,
                 include_only: Optional[List[str]]      = None,
                 no_default_ignore: bool                = False):

        self.root_path                  = Path(root_path).resolve()
        self.max_file_size              = max_file_size
        self.show_tree                  = show_tree
        self.show_tree_size             = show_tree_size
        self.show_line_numbers          = show_line_numbers
        self.show_git_status            = show_git_status
        self.show_permissions           = show_permissions
        self.show_dates                 = show_dates
        self.show_checksums             = show_checksums
        self.filter_by_date             = filter_by_date
        self.search_content             = search_content
        self.show_duplicates            = show_duplicates
        self.sort_by                    = sort_by
        self.max_depth                  = max_depth
        self.include_only               = set(include_only) if include_only else None

        # Build ignore patterns
        self.ignore_patterns = set(DEFAULT_IGNORE) if not no_default_ignore else set()
        if ignore_patterns:
            self.ignore_patterns.update(ignore_patterns)

        # Handle sensitive files
        self.sensitive_patterns = set(SENSITIVE_FILES)
        if view_sensitive:
            for pattern in view_sensitive:
                self.sensitive_patterns.discard(pattern)
        # Statistics
        self.file_count         = 0
        self.dir_count          = 0
        self.skipped_count      = 0
        self.total_size         = 0
        # Initialize features
        self.git_manager        = GitStatusManager(self.root_path) if show_git_status else None
        self.checksum_manager   = ChecksumManager(checksum_type) if show_checksums else None

    def get_tree_structure(self, directory: Path, prefix: str = "", depth: int = 0) -> List[str]:
        """Generate the tree structure"""
        if self.max_depth is not None and depth > self.max_depth:
            return []

        lines = []
        try:
            entries = list(directory.iterdir())
            entries = [e for e in entries if not self._should_ignore(e)]
            entries = sort_entries(entries, self.sort_by)

            # Calculate max length for alignment
            max_len = 0
            if self.show_permissions or self.show_dates or self.show_git_status or self.show_checksums:
                for entry in entries:
                    if entry.is_file():
                        entry_str = entry.name
                        if self.show_tree_size:
                            entry_str += f" ({format_size(entry.stat().st_size)})"
                        max_len = max(max_len, len(entry_str))

            for i, entry in enumerate(entries):
                is_last             = i == len(entries) - 1
                current_prefix      = "└── " if is_last else "├── "
                line                = f"{prefix}{current_prefix}{entry.name}"

                if entry.is_dir():
                    self.dir_count += 1
                    line += "/"
                else:
                    self.file_count += 1
                    size = entry.stat().st_size
                    self.total_size += size

                    # Build base line with size
                    base_line = entry.name
                    if self.show_tree_size:
                        base_line += f" ({format_size(size)})"

                    # Calculate padding for alignment
                    padding     = max_len - len(base_line) if max_len > 0 else 0
                    line        = f"{prefix}{current_prefix}{base_line}{' ' * padding}"

                    # Add aligned metadata
                    metadata = []

                    if self.show_permissions:
                        metadata.append(f"[{get_permissions(entry)}]")

                    if self.show_dates:
                        metadata.append(f"[{get_file_dates(entry)}]")

                    if self.show_git_status and self.git_manager:
                        git_status = self.git_manager.get_status(entry)
                        if git_status:
                            metadata.append(git_status)

                    if self.show_checksums and self.checksum_manager:
                        checksum = self.checksum_manager.calculate(entry)
                        if checksum:
                            metadata.append(f"[{checksum}]")

                    if metadata:
                        line += "  " + " ".join(metadata)

                lines.append(line)

                if entry.is_dir():
                    extension = "    " if is_last else "│   "
                    lines.extend(self.get_tree_structure(entry, prefix + extension, depth + 1))

        except PermissionError:
            self.skipped_count += 1
            lines.append(f"{prefix}[Permission denied]")

        return lines

    def _should_ignore(self, path: Path) -> bool:
        """Check if path should be ignored"""
        include = self.include_only if self.include_only is not None else set()

        if should_ignore(path, self.ignore_patterns, self.sensitive_patterns, include):
            return True

        if path.is_file() and self.filter_by_date and not matches_date_filter(path, self.filter_by_date):
            return True

        return False

    def generate_file_contents(self, directory: Path, depth: int = 0) -> None:
        """Generate content of all files"""
        if self.max_depth is not None and depth > self.max_depth:
            return

        try:
            entries = list(directory.iterdir())
            entries = [e for e in entries if not self._should_ignore(e)]
            entries = sort_entries(entries, self.sort_by)

            for entry in entries:
                if entry.is_dir():
                    self.generate_file_contents(entry, depth + 1)
                else:
                    if self.search_content and not search_in_file(entry, self.search_content):
                        continue

                    relative_path = entry.relative_to(self.root_path)
                    content = read_file_content(entry, self.max_file_size, 
                                               self.show_line_numbers, self.search_content)

                    print(f"\nPath: {relative_path}")
                    print("─" * 70)
                    print(content)
                    print("─" * 27 + "END OF FILE" + "─" * 32)

        except PermissionError:
            pass

    def run(self) -> int:
        """Execute TreeCatt"""
        if not self.root_path.exists():
            print(f"Error: Path '{self.root_path}' does not exist.", file=sys.stderr)
            return 1

        if not self.root_path.is_dir():
            print(f"Error: '{self.root_path}' is not a directory.", file=sys.stderr)
            return 1

        print(f"\nTreeCatt v{VERSION}")
        print(f"Analyzing: {self.root_path}\n")

        # Display tree
        print(f"{self.root_path.name}/")
        tree_lines = self.get_tree_structure(self.root_path)
        for line in tree_lines:
            print(line)

        print(f"\nStatistics:")
        print(f"  - {self.dir_count} directories")
        print(f"  - {self.file_count} files")
        print(f"  - Total size: {format_size(self.total_size)}")
        if self.skipped_count > 0:
            print(f"  - {self.skipped_count} items skipped (permissions)")

        # Display duplicates
        if self.show_duplicates and self.checksum_manager:
            self.checksum_manager.print_duplicates(self.root_path)

        # Display file contents if requested
        if not self.show_tree:
            print(f"\nFile contents:\n")
            print("=" * 70)
            self.generate_file_contents(self.root_path)

        return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description         = 'TreeCatt - Display directory tree and file contents',
        formatter_class     = argparse.RawDescriptionHelpFormatter,
        epilog              = """
Examples:
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
      Show project tree while ignoring build artifacts.

  treecatt --view .env --line-numbers --search "API_KEY"
      Inspect environment files and search for API keys.


MISC
----
  treecatt --version
      Display TreeCatt version information.
        """
    )

    parser.add_argument('path', nargs='?', default=os.getcwd(), 
                       help='Path to analyze (default: .)')

    parser.add_argument('--ignore', '-i', nargs='+', metavar='PATTERN',
                       help='Additional patterns to ignore')

    parser.add_argument('--view', '-v', nargs='+', metavar='FILE',
                       help='Sensitive files to display')

    parser.add_argument('--tree', '-t', action='store_true',
                       help='Display only tree')

    parser.add_argument('--tree-size', action='store_true',
                       help='Show file sizes in tree')

    parser.add_argument('--line-numbers', '-n', action='store_true',
                       help='Display line numbers')

    parser.add_argument('--git-status', '-g', action='store_true',
                       help='Show git status')

    parser.add_argument('--permissions', '-p', action='store_true',
                       help='Show Unix permissions')

    parser.add_argument('--dates', action='store_true',
                       help='Show modification dates')

    parser.add_argument('--checksums', choices=['md5', 'sha1', 'sha256'],
                       help='Calculate checksums')

    parser.add_argument('--duplicates', action='store_true',
                       help='Detect duplicate files')

    parser.add_argument('--search', metavar='PATTERN',
                       help='Search pattern in files')

    parser.add_argument('--filter-date', metavar='TIME',
                       help='Filter by time (7d, 24h, 2w)')

    parser.add_argument('--sort', choices=['name', 'size', 'date', 'ext'], default='name',
                       help='Sort by (default: name)')

    parser.add_argument('--max-size', '-s', default='1MB',
                       help='Max file size (default: 1MB)')

    parser.add_argument('--depth', '-d', type=int,
                       help='Maximum tree depth')

    parser.add_argument('--include', nargs='+', metavar='PATTERN',
                       help='Include only matching files')

    parser.add_argument('--no-default-ignore', action='store_true',
                       help='Disable default ignores')

    parser.add_argument('--version', action='version', version=f'TreeCatt {VERSION}')

    args = parser.parse_args()

    # Validation
    if args.duplicates and not args.checksums:
        args.checksums = 'md5'

    # Convert max size
    max_size    = args.max_size.upper()
    multiplier  = 1
    if max_size.endswith('KB'):
        multiplier  = 1024
        max_size    = max_size[:-2]
    elif max_size.endswith('MB'):
        multiplier  = 1024 * 1024
        max_size    = max_size[:-2]
    elif max_size.endswith('GB'):
        multiplier  = 1024 * 1024 * 1024
        max_size    = max_size[:-2]

    try:
        max_file_size = int(float(max_size) * multiplier)
    except ValueError:
        print(f"Error: Invalid size '{args.max_size}'", file=sys.stderr)
        return 1
    
    treecatt = TreeCatt(
        root_path               = args.path,
        ignore_patterns         = args.ignore,
        view_sensitive          = args.view,
        max_file_size           = max_file_size,
        show_tree               = args.tree,
        show_tree_size          = args.tree_size,
        show_line_numbers       = args.line_numbers,
        show_git_status         = args.git_status,
        show_permissions        = args.permissions,
        show_dates              = args.dates,
        show_checksums          = bool(args.checksums),
        checksum_type           = args.checksums or 'md5',
        filter_by_date          = args.filter_date,
        search_content          = args.search,
        show_duplicates         = args.duplicates,
        sort_by                 = args.sort,
        max_depth               = args.depth,
        include_only            = args.include,
        no_default_ignore       = args.no_default_ignore
    )

    return treecatt.run()


if __name__ == '__main__':
    sys.exit(main())