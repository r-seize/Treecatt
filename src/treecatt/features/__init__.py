"""
TreeCatt features module
"""

from .git import GitStatusManager
from .file import (
    is_binary_file,
    read_file_content,
    search_in_file,
    get_permissions,
    get_file_dates,
    format_size,
)
from .filter import (
    should_ignore,
    sort_entries,
)

__all__ = [
    'GitStatusManager',
    'is_binary_file',
    'read_file_content',
    'search_in_file',
    'get_permissions',
    'get_file_dates',
    'format_size',
    'should_ignore',
    'sort_entries',
]