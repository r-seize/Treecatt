"""
File utility functions for TreeCatt
"""

from calendar import week
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Union
from treecatt.constants import BINARY_EXTENSIONS

def is_binary_file(path: Path) -> Optional[bool]:
    """Determine if a file is binary(like cat does)"""

    if path.suffix.lower() in BINARY_EXTENSIONS:
        return True

    try:
        with open(path, 'rb') as f:
            chunk = f.read(8192)

            if not chunk:
                return False

            if b'\x00' in chunk:
                return True

            text_chars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
            no_text    = chunk.translate(None, text_chars)

            if len(no_text) / len(chunk) > 0.3:
                return True

            return False
    except:
        return True

def get_permissions(path: Path) -> Optional[str]:
    """Returns the Unix permissions of the file"""
    try:
        stat_info   = path.stat()
        mode        = stat_info.st_mode

        perms = ''
        perms += 'r' if mode & 0o400 else '-'
        perms += 'w' if mode & 0o200 else '-'
        perms += 'x' if mode & 0o100 else '-'
        perms += 'r' if mode & 0o040 else '-'
        perms += 'w' if mode & 0o020 else '-'
        perms += 'x' if mode & 0o010 else '-'
        perms += 'r' if mode & 0o004 else '-'
        perms += 'w' if mode & 0o002 else '-'
        perms += 'x' if mode & 0o001 else '-'

        return perms
    except:
        return "---------"

def format_size(size: float) -> str:
    """Format size in readable units"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f}{unit}"
        size /= 1024.0
    return f"{size:.1f}TB"

def matches_date_filter(path: Path, filter_spec: Optional[str]) -> bool:
    """Check if the file matches the date filter"""
    if not filter_spec:
        return True

    try:
        stat_info   = path.stat()
        mtime       = datetime.fromtimestamp(stat_info.st_mtime)
        now         = datetime.now()

        if filter_spec.endswith('d'):
            days = int(filter_spec[:-1])
            return (now - mtime).days <= days
        elif filter_spec.endswith('h'):
            hours = int(filter_spec[:-1])
            return (now - mtime).total_seconds() / 3600 <= hours
        elif filter_spec.endswith('w'):
            weeks = int(filter_spec[:-1])
            return (now - mtime).days <= weeks * 7
    except:
        pass

    return True

def read_file_content(
    file_path: Path,
    max_size: float,
    show_line_numbers: bool         = False, 
    search_content: Optional[str]   =  None
    ) -> Optional[str]:
    """Read file content (like cat does)"""

    try:
        size = file_path.stat().st_size

        if size > max_size:
            return f"[File to large: {format_size(size)}]"

        if is_binary_file(file_path):
            return f"[Binary file]"

        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1', errors='replace') as f:
                content = f.read()

        if search_content and search_content.lower() in content.lower():
            lines               = content.split('\n')
            highlighted_lines   = []
            for i, line in enumerate(lines):
                if search_content.lower() in line.lower():
                    if show_line_numbers:
                        highlighted_lines.append(f"{i+1:4d} | {line}")
                    else:
                        highlighted_lines.append(f"{line}")
                else:
                    if show_line_numbers:
                        highlighted_lines.append(f"{i+1:4d} | {line}")
                    else:
                        highlighted_lines.append(line)
            return '\n'.join(highlighted_lines)

        if show_line_numbers:
            lines           = content.split('\n')
            numbered_lines  = [f"{i+1:4d} | {line}" for i, line in enumerate(lines)]
            return '\n'.join(numbered_lines)

        return content

    except PermissionError:
        return "[Permission denied]"
    except Exception as e:
        return f"[Read error: {str(e)}]"

def get_file_dates(path: Union[Path, str]) -> str:
    try:
        p           = Path(path)
        stat_info   = p.stat()
        mtime       = datetime.fromtimestamp(stat_info.st_mtime, tz=timezone.utc)
        return mtime.strftime('%Y-%m-%d %H:%M')
    except (OSError, ValueError, TypeError):
        return "N/A"