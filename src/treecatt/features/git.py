"""
Git integration features for TreeCatt
"""

import subprocess
from pathlib import Path
from typing import Dict, Optional

class GitStatusManager:
    """Manages Git status information for files"""

    def __init__(self, root_path: Path):
        self.root_path                      = root_path
        self.status_cache: Dict[str, str]   = {}
        self._cache_git_status()


    def _cache_git_status(self):
        """Cache the Git status of files"""
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd                     = self.root_path,
                capture_output          = True,
                text                    = True,
                timeout                 = 5
            )
            for line in result.stdout.splitlines():
                if len(line) > 3:
                    status                          = line[:2]
                    filepath                        = line[3:]
                    self.status_cache[filepath]     = status
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
            pass

    def get_status(self, path: Path) -> Optional[str]:
        """Returns the Git status of a file"""
        if not self.status_cache:
            return ""

        try:
            rel_path    = str(path.relative_to(self.root_path))
            status      = self.status_cache.get(rel_path, "")

            status_map  = {
                'M ': '[M]', # Modified
                ' M': '[M]',
                'A ': '[A]', # Added
                'D' : '[D]', # Deleted
                'R' : '[R]', # Renamed
                '??': '[?]', # Untracked
                'MM': '[M]',
            }

            return status_map.get(status.strip(), "")
        except ValueError:
            return ""
