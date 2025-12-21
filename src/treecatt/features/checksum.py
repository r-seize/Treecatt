"""
Checksum calculation and duplicate detection for TreeCatt
"""

import hashlib
from pathlib import Path
from typing import Dict, List, Optional

class ChecksumManager:
    """Manages file checksums and duplicate detection"""

    def __init__(self, checksum_type: str = 'md5'):
        self.checksum_type                          = checksum_type
        self.file_checksums: Dict[str, List[Path]]  = {}

    def calculate(self, path: Path) -> Optional[str]:
        """Calculate the checksum of a file"""
        try:
            if self.checksum_type == 'md5':
                hasher = hashlib.md5()
            elif self.checksum_type == 'sha1':
                hasher = hashlib.sha1()
            elif self.checksum_type == 'sha256':
                hasher = hashlib.sha256()
            else:
                return ""

            with open(path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)

            checksum = hasher.hexdigest()

            if checksum in self.file_checksums:
                self.file_checksums[checksum].append(path)
            else:
                self.file_checksums[checksum] = [path]

            return checksum[:8]
        except:
            return ""

    def get_duplicates(self) -> Dict[str, List[Path]]:
        """Returnrs file with duplicate checknums"""
        return {k: v for k, v in self.file_checksums.items() if len(v) > 1}

    def format_size(self, size: float) -> str:
        """Format size in readable units"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f}{unit}"
            size /= 1024.0
        return f"{size:.1f}TB"

    def print_duplicates(self, root_path: Path):
        """Print duplicate files report"""
        duplicates = self.get_duplicates()

        if not duplicates:
            return

        print("\nDuplicate files found:")
        print("-" * 70)
        for checksum, files in duplicates.items():
            print(f"\nChecksum: {checksum}")
            total_wasted = sum(f.stat().st_size for f in files[1:])
            print(f"Wasted space: {self.format_size(total_wasted)}")
            for f in files:
                print(f"  - {f.relative_to(root_path)} ({self.format_size(f.stat().st_size)})")