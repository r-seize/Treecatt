"""
Core TreeCatt class
"""

import sys
from pathlib import Path
from typing import List, Optional

from treecatt.constants import DEFAULT_IGNORE, SENSITIVE_FILES
from treecatt.features import (
    GitStatusManager, ChecksumManager,
    format_size, get_permissions, get_file_dates, matches_date_filter,
    read_file_content, should_ignore, search_in_file, sort_entries
)


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
        # Build include set (None if not specified)
        include = self.include_only if self.include_only is not None else None

        # Use the should_ignore function with proper parameters
        if should_ignore(path, self.ignore_patterns, self.sensitive_patterns, include):
            return True

        # Apply date filter to files
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
                    # Skip files that don't match search pattern
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

    def print_header(self, version: str) -> None:
        """Print TreeCatt header"""
        print(f"\nTreeCatt v{version}")
        print(f"Analyzing: {self.root_path}\n")

    def print_tree(self) -> None:
        """Print directory tree"""
        print(f"{self.root_path.name}/")
        tree_lines = self.get_tree_structure(self.root_path)
        for line in tree_lines:
            print(line)

    def print_statistics(self) -> None:
        """Print file statistics"""
        print(f"\nStatistics:")
        print(f"  - {self.dir_count} directories")
        print(f"  - {self.file_count} files")
        print(f"  - Total size: {format_size(self.total_size)}")
        if self.skipped_count > 0:
            print(f"  - {self.skipped_count} items skipped (permissions)")

    def print_duplicates(self) -> None:
        """Print duplicate files if enabled"""
        if self.show_duplicates and self.checksum_manager:
            self.checksum_manager.print_duplicates(self.root_path)

    def print_file_contents(self) -> None:
        """Print file contents if not in tree-only mode"""
        if not self.show_tree:
            print(f"\nFile contents:\n")
            print("=" * 70)
            self.generate_file_contents(self.root_path)

    def run(self) -> int:
        """Execute TreeCatt"""
        if not self.root_path.exists():
            print(f"Error: Path '{self.root_path}' does not exist.", file=sys.stderr)
            return 1

        if not self.root_path.is_dir():
            print(f"Error: '{self.root_path}' is not a directory.", file=sys.stderr)
            return 1

        # Print header
        from treecatt import __version__
        self.print_header(__version__)

        # Display tree
        self.print_tree()

        # Display statistics
        self.print_statistics()

        # Display duplicates
        self.print_duplicates()

        # Display file contents if requested
        self.print_file_contents()

        return 0