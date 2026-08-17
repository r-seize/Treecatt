"""
File utility functions for TreeCatt
"""

from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Union

BINARY_EXTENSIONS = {
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.webp', '.tiff', '.psd',
    '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm',
    '.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a',
    '.zip', '.tar', '.gz', '.bz2', '.xz', '.7z', '.rar', '.iso',
    '.exe', '.dll', '.so', '.dylib', '.bin', '.app',
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
    '.db', '.sqlite', '.sqlite3', '.mdb',
    '.pyc', '.pyo', '.pyd', '.class', '.o', '.obj', '.a', '.lib',
    '.ttf', '.otf', '.woff', '.woff2', '.eot',
    '.swf', '.jar', '.war', '.ear',
}


def is_binary_file(path: Path) -> bool:
    """Determine if a file is binary"""
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
            no_text = chunk.translate(None, text_chars)
            return len(no_text) / len(chunk) > 0.3
    except Exception:
        return True


def read_file_content(file_path: Path, max_size: int = 1024 * 1024) -> Optional[str]:
    """Read and return file content, or a placeholder for binary/large files"""
    try:
        size = file_path.stat().st_size
        if size > max_size:
            return f"[File too large: {format_size(size)}]"
        if is_binary_file(file_path):
            return "[Binary file]"
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                return f.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1', errors='replace') as f:
                return f.read()
    except PermissionError:
        return "[Permission denied]"
    except Exception as e:
        return f"[Read error: {e}]"


def get_permissions(path: Path) -> str:
    """Returns the Unix permissions of the file"""
    try:
        mode = path.stat().st_mode
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
    except Exception:
        return "---------"


def format_size(size: float) -> str:
    """Format size in readable units"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f}{unit}"
        size /= 1024.0
    return f"{size:.1f}TB"


def search_in_file(file_path: Path, pattern: str) -> bool:
    """Return True if pattern is found in file content."""
    content = read_file_content(file_path)
    if not content or content.startswith('['):
        return False
    return pattern in content


def get_file_dates(path: Union[Path, str]) -> str:
    """Get formatted modification date of a file"""
    try:
        p = Path(path)
        mtime = datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc)
        return mtime.strftime('%Y-%m-%d %H:%M')
    except Exception:
        return "N/A"