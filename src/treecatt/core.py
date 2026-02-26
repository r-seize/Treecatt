"""
Core TreeCatt class
"""

import sys
from pathlib import Path
from typing import List, Optional

from treecatt.constants import DEFAULT_IGNORE
from treecatt.features import (
    GitStatusManager,
    format_size,
    get_permissions,
    get_file_dates,
    read_file_content,
    should_ignore,
    sort_entries,
)
from treecatt.colors import (
    bold, dim, blue, cyan, green, yellow, magenta, red,
    bright_blue, bright_cyan, bright_green, bright_yellow, bright_white,
)

# Tree drawing characters
ELBOW = dim("└── ")
TEE   = dim("├── ")
BLANK = "    "
VERT  = dim("│   ")

# Extension → color mapping
EXT_COLORS = {
    ".py": bright_blue, ".pyi": blue,
    ".js": bright_yellow, ".mjs": bright_yellow,
    ".ts": blue, ".tsx": cyan, ".jsx": cyan,
    ".html": yellow, ".htm": yellow,
    ".css": magenta, ".scss": magenta, ".sass": magenta,
    ".json": bright_yellow,
    ".yaml": yellow, ".yml": yellow, ".toml": yellow,
    ".ini": yellow, ".cfg": yellow, ".conf": yellow,
    ".sh": bright_green, ".bash": bright_green, ".zsh": bright_green,
    ".md": cyan, ".rst": cyan, ".txt": bright_white,
    ".c": bright_blue, ".h": blue, ".cpp": bright_blue, ".hpp": blue,
    ".rs": yellow, ".go": cyan, ".rb": red, ".php": magenta,
    ".java": yellow, ".kt": magenta,
    "Makefile": bright_green, "makefile": bright_green, ".mk": bright_green,
}

GIT_COLORS = {
    "[M]": yellow,
    "[A]": bright_green,
    "[D]": red,
    "[R]": cyan,
    "[?]": dim,
}


def color_filename(path: Path) -> str:
    """Return a colorized filename based on type/extension"""
    name = path.name
    if path.is_dir():
        return bold(bright_blue(name))
    try:
        import stat as _stat
        if path.stat().st_mode & (_stat.S_IXUSR | _stat.S_IXGRP | _stat.S_IXOTH):
            return bright_green(name)
    except Exception:
        pass
    fn = EXT_COLORS.get(path.suffix.lower()) or EXT_COLORS.get(name)
    if fn:
        return fn(name)
    return bright_white(name)


def color_size(s: str) -> str:
    return dim(f"({s})")


def color_perms(p: str) -> str:
    result = ""
    for ch in p:
        if ch == "-":
            result += dim(ch)
        elif ch in "rwx":
            result += bright_green(ch)
        else:
            result += ch
    return f"[{result}]"


def color_date(d: str) -> str:
    return dim(f"[{d}]")


def color_git(status: str) -> str:
    fn = GIT_COLORS.get(status, lambda x: x)
    return fn(status)


class TreeCatt:
    """Main TreeCatt class for tree generation and file content display"""

    def __init__(
        self,
        root_path: str,
        show_tree_only: bool = False,
        show_tree_size: bool = False,
        show_permissions: bool = False,
        show_dates: bool = False,
        show_git_status: bool = False,
        sort_by: str = 'name',
        max_depth: Optional[int] = None,
        max_file_size: int = 1024 * 1024,
    ):
        self.root_path = Path(root_path).resolve()
        self.show_tree_only = show_tree_only
        self.show_tree_size = show_tree_size
        self.show_permissions = show_permissions
        self.show_dates = show_dates
        self.show_git_status = show_git_status
        self.sort_by = sort_by
        self.max_depth = max_depth
        self.max_file_size = max_file_size

        self.ignore_patterns = set(DEFAULT_IGNORE)

        self.file_count = 0
        self.dir_count = 0
        self.total_size = 0

        self.git_manager = GitStatusManager(self.root_path) if show_git_status else None

    def _should_ignore(self, path: Path) -> bool:
        return should_ignore(path, self.ignore_patterns)

    def get_tree_structure(self, directory: Path, prefix: str = "", depth: int = 0) -> List[str]:
        """Generate the tree structure"""
        if self.max_depth is not None and depth > self.max_depth:
            return []

        lines = []
        try:
            entries = [e for e in directory.iterdir() if not self._should_ignore(e)]
            entries = sort_entries(entries, self.sort_by)

            show_meta = self.show_permissions or self.show_dates or self.show_git_status

            # Pre-calculate max plain-text length for metadata alignment
            max_len = 0
            if show_meta:
                for entry in entries:
                    if entry.is_file():
                        plain = entry.name
                        if self.show_tree_size:
                            plain += f" ({format_size(entry.stat().st_size)})"
                        max_len = max(max_len, len(plain))

            for i, entry in enumerate(entries):
                is_last = i == len(entries) - 1
                connector = ELBOW if is_last else TEE

                if entry.is_dir():
                    self.dir_count += 1
                    lines.append(f"{prefix}{connector}{color_filename(entry)}/")
                    ext = BLANK if is_last else VERT
                    lines.extend(self.get_tree_structure(entry, prefix + ext, depth + 1))
                else:
                    self.file_count += 1
                    size = entry.stat().st_size
                    self.total_size += size

                    plain_base = entry.name
                    if self.show_tree_size:
                        plain_base += f" ({format_size(size)})"

                    colored_name = color_filename(entry)
                    if self.show_tree_size:
                        colored_name += " " + color_size(format_size(size))

                    if show_meta:
                        padding = max_len - len(plain_base)
                        line = f"{prefix}{connector}{colored_name}{' ' * padding}"
                        meta = []
                        if self.show_permissions:
                            meta.append(color_perms(get_permissions(entry)))
                        if self.show_dates:
                            meta.append(color_date(get_file_dates(entry)))
                        if self.show_git_status and self.git_manager:
                            gs = self.git_manager.get_status(entry)
                            if gs:
                                meta.append(color_git(gs))
                        if meta:
                            line += "  " + " ".join(meta)
                    else:
                        line = f"{prefix}{connector}{colored_name}"

                    lines.append(line)

        except PermissionError:
            lines.append(f"{prefix}{red('[Permission denied]')}")

        return lines

    def _collect_files(self, directory: Path, depth: int = 0) -> List[Path]:
        """Recursively collect all non-ignored files"""
        if self.max_depth is not None and depth > self.max_depth:
            return []
        files = []
        try:
            entries = [e for e in directory.iterdir() if not self._should_ignore(e)]
            entries = sort_entries(entries, self.sort_by)
            for entry in entries:
                if entry.is_dir():
                    files.extend(self._collect_files(entry, depth + 1))
                else:
                    files.append(entry)
        except PermissionError:
            pass
        return files

    def print_file_contents(self) -> None:
        """Print path + content of every file"""
        files = self._collect_files(self.root_path)
        if not files:
            return

        sep_heavy = dim("=" * 70)
        sep_light = dim("─" * 70)
        sep_end   = dim("─" * 27) + dim("END OF FILE") + dim("─" * 32)

        print(f"\n{bold('File contents:')}\n")
        print(sep_heavy)

        for file_path in files:
            rel = file_path.relative_to(self.root_path)
            content = read_file_content(file_path, self.max_file_size)

            print(f"\n{bold('Path:')} {color_filename(file_path)}  {dim(str(rel.parent) + '/') if str(rel.parent) != '.' else ''}")
            print(sep_light)
            print(content)
            print(sep_end)

    def print_tree(self) -> None:
        """Print the directory tree"""
        print(bold(bright_blue(self.root_path.name)) + "/")
        for line in self.get_tree_structure(self.root_path):
            print(line)

    def print_statistics(self) -> None:
        """Print file statistics"""
        print()
        print(bold("Statistics:"))
        print(f"  {dim('─' * 28)}")
        print(f"  {dim('Directories :')}  {bright_yellow(str(self.dir_count))}")
        print(f"  {dim('Files       :')}  {bright_yellow(str(self.file_count))}")
        print(f"  {dim('Total size  :')}  {bright_yellow(format_size(self.total_size))}")

    def run(self) -> int:
        """Execute TreeCatt"""
        if not self.root_path.exists():
            print(f"{red('Error:')} Path '{self.root_path}' does not exist.", file=sys.stderr)
            return 1
        if not self.root_path.is_dir():
            print(f"{red('Error:')} '{self.root_path}' is not a directory.", file=sys.stderr)
            return 1

        from treecatt import __version__
        print(f"\n{bold('treecatt')} {dim('v' + __version__)}")
        print(f"{dim('Analyzing:')} {cyan(str(self.root_path))}\n")

        self.print_tree()
        self.print_statistics()

        if not self.show_tree_only:
            self.print_file_contents()

        print()
        return 0