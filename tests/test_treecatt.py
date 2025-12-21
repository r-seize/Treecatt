"""
Tests unitaires pour TreeCatt
"""

import pytest
import tempfile
import os
from pathlib import Path
from treecatt.main import TreeCatt

class TestTreeCatt:
    
    @pytest.fixture
    def temp_project(self):
        """Crée une structure de projet temporaire pour les tests"""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            
            # Créer des dossiers
            (base / "src").mkdir()
            (base / "tests").mkdir()
            (base / "node_modules").mkdir()  # Devrait être ignoré
            
            # Créer des fichiers
            (base / "README.md").write_text("# Test Project")
            (base / "src" / "main.py").write_text("print('Hello')")
            (base / "src" / "utils.py").write_text("def hello(): pass")
            (base / "tests" / "test_main.py").write_text("import pytest")
            (base / ".env").write_text("SECRET=123")  # Devrait être ignoré
            (base / "node_modules" / "package.json").write_text("{}")
            
            yield base
    
    def test_initialization(self, temp_project):
        """Test l'initialisation de TreeCatt"""
        tc = TreeCatt(str(temp_project))
        assert tc.root_path == temp_project
        assert tc.file_count == 0
        assert tc.dir_count == 0
    
    def test_ignore_patterns(self, temp_project):
        """Test que les patterns par défaut sont ignorés"""
        tc = TreeCatt(str(temp_project))
        
        # node_modules devrait être ignoré
        assert tc.should_ignore(temp_project / "node_modules")
        
        # .env devrait être ignoré
        assert tc.should_ignore(temp_project / ".env")
        
        # README.md ne devrait pas être ignoré
        assert not tc.should_ignore(temp_project / "README.md")
    
    def test_custom_ignore(self, temp_project):
        """Test les patterns d'ignore personnalisés"""
        tc = TreeCatt(str(temp_project), ignore_patterns=["*.md"])
        
        # README.md devrait maintenant être ignoré
        assert tc.should_ignore(temp_project / "README.md")
    
    def test_view_sensitive(self, temp_project):
        """Test l'affichage de fichiers sensibles"""
        tc = TreeCatt(str(temp_project), view_sensitive=[".env"])
        
        # .env ne devrait plus être ignoré
        assert not tc.should_ignore(temp_project / ".env")
    
    def test_file_count(self, temp_project):
        """Test le comptage des fichiers"""
        tc = TreeCatt(str(temp_project))
        tc.get_tree_structure(temp_project)
        
        # Devrait compter tous les fichiers sauf ceux ignorés
        # README.md, src/main.py, src/utils.py, tests/test_main.py = 4 fichiers
        assert tc.file_count == 4
        
        # src, tests = 2 dossiers (node_modules ignoré)
        assert tc.dir_count == 2
    
    def test_format_size(self, temp_project):
        """Test le formatage des tailles"""
        tc = TreeCatt(str(temp_project))
        
        assert tc.format_size(100) == "100.0B"
        assert tc.format_size(1024) == "1.0KB"
        assert tc.format_size(1024 * 1024) == "1.0MB"
        assert tc.format_size(1024 * 1024 * 1024) == "1.0GB"
    
    def test_read_file_content(self, temp_project):
        """Test la lecture du contenu des fichiers"""
        tc = TreeCatt(str(temp_project))
        
        content = tc.read_file_content(temp_project / "README.md")
        assert "Test Project" in content
        
        content = tc.read_file_content(temp_project / "src" / "main.py")
        assert "print('Hello')" in content
    
    def test_max_file_size(self, temp_project):
        """Test la limite de taille des fichiers"""
        tc = TreeCatt(str(temp_project), max_file_size=10)  # 10 bytes max
        
        # Un fichier plus grand devrait retourner un message
        content = tc.read_file_content(temp_project / "README.md")
        assert "trop volumineux" in content
    
    def test_line_numbers(self, temp_project):
        """Test l'affichage des numéros de ligne"""
        tc = TreeCatt(str(temp_project), show_line_numbers=True)
        
        content = tc.read_file_content(temp_project / "src" / "main.py")
        assert "1 |" in content
    
    def test_max_depth(self, temp_project):
        """Test la limitation de profondeur"""
        tc = TreeCatt(str(temp_project), max_depth=0)
        tree = tc.get_tree_structure(temp_project)
        
        # Avec depth=0, ne devrait voir que le niveau racine
        assert len(tree) == 4  # README.md, src/, tests/, .env (ignoré = 3)
    
    def test_include_only(self, temp_project):
        """Test le filtrage par inclusion"""
        tc = TreeCatt(str(temp_project), include_only=["*.py"])
        
        # Seuls les .py devraient passer
        assert not tc.should_ignore(temp_project / "src" / "main.py")
        assert tc.should_ignore(temp_project / "README.md")
    
    def test_no_default_ignore(self, temp_project):
        """Test la désactivation des ignores par défaut"""
        tc = TreeCatt(str(temp_project), no_default_ignore=True)
        
        # node_modules ne devrait plus être ignoré
        assert not tc.should_ignore(temp_project / "node_modules")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])