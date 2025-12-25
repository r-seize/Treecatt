"""
Unit tests for TreeCatt
"""

import pytest
import tempfile
from pathlib import Path
from typing import Generator
from treecatt.main import TreeCatt
from treecatt.features import format_size, get_permissions, should_ignore, sort_entries


class TestTreeCatt:

    @pytest.fixture
    def temp_project(self) -> Generator[Path, None, None]:
        """Create a temporary project structure for tests"""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)

            (base / "src").mkdir()
            (base / "tests").mkdir()
            (base / "node_modules").mkdir()
            (base / "README.md").write_text("# Test Project")
            (base / "src" / "main.py").write_text("print('Hello')\n# TODO: fix this")
            (base / "src" / "utils.py").write_text("def hello(): pass")
            (base / "tests" / "test_main.py").write_text("import pytest")
            (base / ".env").write_text("SECRET=123")
            (base / "node_modules" / "package.json").write_text("{}")
            (base / "large.txt").write_text("x" * 2000)

            yield base

    def test_initialization(self, temp_project: Path) -> None:
        """Test TreeCatt initialization"""
        tc                      = TreeCatt(str(temp_project))
        assert tc.root_path     == temp_project
        assert tc.file_count    == 0
        assert tc.dir_count     == 0
        assert tc.show_tree is False
        assert tc.show_tree_size is False

    def test_ignore_patterns(self, temp_project: Path) -> None:
        """Test default ignore patterns"""
        tc = TreeCatt(str(temp_project))
        assert tc._should_ignore(temp_project / "node_modules")
        assert tc._should_ignore(temp_project / ".env")
        assert tc._should_ignore(temp_project / "README.md")
        assert not tc._should_ignore(temp_project / "src" / "main.py")

    def test_custom_ignore(self, temp_project: Path) -> None:
        """Test custom ignore patterns"""
        tc = TreeCatt(str(temp_project), ignore_patterns=["*.txt"])
        assert tc._should_ignore(temp_project / "large.txt")

    def test_view_sensitive(self, temp_project: Path) -> None:
        """Test viewing sensitive files"""
        tc = TreeCatt(str(temp_project), view_sensitive=[".env"])
        assert not tc._should_ignore(temp_project / ".env")

    def test_tree_structure(self, temp_project: Path) -> None:
        """Test tree structure generation"""
        tc                      = TreeCatt(str(temp_project))
        tree_lines              = tc.get_tree_structure(temp_project)
        assert tc.dir_count     == 2
        assert tc.file_count    >= 3
        assert len(tree_lines)  > 0
    
    def test_tree_with_size(self, temp_project: Path) -> None:
        """Test tree with file sizes"""
        tc              = TreeCatt(str(temp_project), show_tree=True, show_tree_size=True)
        tree_lines      = tc.get_tree_structure(temp_project)
        has_size        = any("KB" in line or "B)" in line for line in tree_lines)
        assert has_size

    def test_format_size(self) -> None:
        """Test size formatting"""
        assert format_size(100)                 == "100.0B"
        assert format_size(1024)                == "1.0KB"
        assert format_size(1024 * 1024)         == "1.0MB"
        assert format_size(1024 * 1024 * 1024)  == "1.0GB"

    def test_max_depth(self, temp_project: Path) -> None:
        """Test maximum depth limitation"""
        tc                  = TreeCatt(str(temp_project), max_depth=0)
        tree                = tc.get_tree_structure(temp_project)
        assert len(tree)    <= 5

    def test_include_only(self, temp_project: Path) -> None:
        """Test include-only filtering"""
        tc = TreeCatt(str(temp_project), include_only=["*.py"])
        assert not tc._should_ignore(temp_project / "src" / "main.py")
        assert tc._should_ignore(temp_project / "large.txt")

    def test_no_default_ignore(self, temp_project: Path) -> None:
        """Test disabling default ignores"""
        tc = TreeCatt(str(temp_project), no_default_ignore=True)
        assert not tc._should_ignore(temp_project / "node_modules")

    def test_sort_by_name(self, temp_project: Path) -> None:
        """Test sorting by name"""
        tc                  = TreeCatt(str(temp_project), sort_by='name')
        entries             = list((temp_project / "src").iterdir())
        sorted_entries      = sort_entries(entries, 'name')
        assert sorted_entries[0].name <= sorted_entries[-1].name

    def test_sort_by_size(self, temp_project: Path) -> None:
        """Test sorting by size"""
        tc                  = TreeCatt(str(temp_project), sort_by='size')
        entries             = list(temp_project.iterdir())
        files               = [e for e in entries if e.is_file()]
        sorted_entries      = sort_entries(files, 'size')

        if len(sorted_entries) > 1:
            assert sorted_entries[0].stat().st_size >= sorted_entries[-1].stat().st_size

    def test_permissions(self, temp_project: Path) -> None:
        """Test permissions display"""
        test_file   = temp_project / "src" / "main.py"
        perms       = get_permissions(test_file)

        assert perms is not None
        assert len(perms) == 9
        assert perms[0] in ['r', '-']
        assert perms[1] in ['w', '-']
        assert perms[2] in ['x', '-']

    def test_search_content(self, temp_project: Path) -> None:
        """Test content search"""
        from treecatt.features import search_in_file

        result1 = search_in_file(temp_project / "src" / "main.py", "TODO")
        result2 = search_in_file(temp_project / "src" / "utils.py", "TODO")

        assert result1 is True
        assert result2 is False

    def test_max_file_size(self, temp_project: Path) -> None:
        """Test max file size limitation"""
        from treecatt.features import read_file_content

        content = read_file_content(temp_project / "large.txt", 100)
        assert content is not None
        assert "large" in content.lower()

    def test_git_status_manager(self, temp_project: Path) -> None:
        """Test Git status manager initialization"""
        tc = TreeCatt(str(temp_project), show_git_status=True)
        assert tc.git_manager is not None

    def test_checksum_manager(self, temp_project: Path) -> None:
        """Test checksum manager"""
        tc = TreeCatt(str(temp_project), show_checksums=True, checksum_type='md5')
        assert tc.checksum_manager is not None
        assert tc.checksum_manager.checksum_type == 'md5'

    def test_run_success(self, temp_project: Path) -> None:
        """Test successful run"""
        tc                      = TreeCatt(str(temp_project), show_tree=True)
        result                  = tc.run()
        assert result           == 0
        assert tc.file_count    > 0
        assert tc.dir_count     > 0
    
    def test_run_nonexistent_path(self) -> None:
        """Test run with nonexistent path"""
        tc              = TreeCatt("/nonexistent/path")
        result          = tc.run()
        assert result   == 1

    def test_statistics(self, temp_project: Path) -> None:
        """Test statistics collection"""
        tc = TreeCatt(str(temp_project))
        tc.get_tree_structure(temp_project)
        assert tc.file_count    > 0
        assert tc.dir_count     > 0
        assert tc.total_size    > 0


class TestFeatures:
    """Test individual features"""

    def test_should_ignore_with_patterns(self) -> None:
        """Test should_ignore function"""
        path        = Path("/test/node_modules")
        result      = should_ignore(path, {'node_modules'}, set(), None)
        assert result is True

    def test_sort_entries_by_extension(self, tmp_path: Path) -> None:
        """Test sorting by extension"""
        (tmp_path / "file.py").touch()
        (tmp_path / "file.js").touch()
        (tmp_path / "file.txt").touch()

        entries = list(tmp_path.iterdir())
        sorted_entries = sort_entries(entries, 'ext')
        assert len(sorted_entries) == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])