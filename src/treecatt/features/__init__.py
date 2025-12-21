"""
TreeCatt features module
"""

from .git import GitStatusManager
from .checksum import ChecksumManager
from .file import (
    is_binary_file,
    get_permissions,
    get_file_dates,
    format_size,
    matches_date_filter,
    read_file_content
)
from .filter import (
    should_ignore,
    search_in_file,
    sort_entries
)

__all__ = [
    'GitStatusManager',
    'ChecksumManager',
    'is_binary_file',
    'get_permissions',
    'get_file_dates',
    'format_size',
    'matches_date_filter',
    'read_file_content',
    'should_ignore',
    'search_in_file',
    'sort_entries'
]