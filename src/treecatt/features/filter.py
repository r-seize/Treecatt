"""
Filter and search utilities for TreeCatt
"""

import fnmatch
from pathlib import Path
from typing import Set, List, Optional
from treecatt.features.file import is_binary_file


def should_ignore(path: Path, ignore_patterns: Set[str], sensitive_patterns: Set[str],
                  include_only: Optional[Set[str]] = None) -> bool:
    """Check if a path should be ignored"""
    name = path.name

    for pattern in ignore_patterns:
        if fnmatch.fnmatch(name, pattern):
            return True

    for pattern in sensitive_patterns:
        if fnmatch.fnmatch(name, pattern):
            return True

    if include_only:
        included = False
        for pattern in include_only:
            if fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(str(path), f"*{pattern}*"):
                included = True
                break
        if not included:
            return True

    return False


def search_in_file(path: Path, search_pattern: str) -> bool:
    """Search for a pattern in file content"""
    if not search_pattern:
        return False

    try:
        if is_binary_file(path):
            return False

        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            return search_pattern.lower() in content.lower()
    except:
        return False


def sort_entries(entries: List[Path], sort_by: str) -> List[Path]:
    """Sort entries by specified criteria"""
    if sort_by == 'size':
        return sorted(entries, key=lambda x: (not x.is_dir(), -x.stat().st_size if x.is_file() else 0, x.name.lower()))
    elif sort_by == 'date':
        return sorted(entries, key=lambda x: (not x.is_dir(), -x.stat().st_mtime, x.name.lower()))
    elif sort_by == 'ext':
        return sorted(entries, key=lambda x: (not x.is_dir(), x.suffix.lower(), x.name.lower()))
    else:  # name (default)
        return sorted(entries, key=lambda x: (not x.is_dir(), x.name.lower()))