"""
Filter and sort utilities for TreeCatt
"""

import fnmatch
from pathlib import Path
from typing import Set, List


def should_ignore(path: Path, ignore_patterns: Set[str]) -> bool:
    """Determine if a path should be ignored."""
    name = path.name
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(name, pattern):
            return True
    return False


def sort_entries(entries: List[Path], sort_by: str) -> List[Path]:
    """Sort entries by specified criteria"""
    if sort_by == 'size':
        return sorted(
            entries,
            key=lambda x: (not x.is_dir(), -x.stat().st_size if x.is_file() else 0, x.name.lower())
        )
    elif sort_by == 'date':
        return sorted(
            entries,
            key=lambda x: (not x.is_dir(), -x.stat().st_mtime, x.name.lower())
        )
    elif sort_by == 'ext':
        return sorted(
            entries,
            key=lambda x: (not x.is_dir(), x.suffix.lower(), x.name.lower())
        )
    else:  # name (default)
        return sorted(
            entries,
            key=lambda x: (not x.is_dir(), x.name.lower())
        )