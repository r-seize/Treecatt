"""
TreeCatt - Un outil moderne pour afficher l'arborescence et le contenu des fichiers

TreeCatt combine les fonctionnalités de 'tree' et 'cat' pour analyser
rapidement la structure d'un projet et le contenu de ses fichiers.
"""

__version__     = "0.1.2"
__author__      = "TreeCatt Developer"
__license__     = "MIT"

from .main import TreeCatt, main

__all__ = ["TreeCatt", "main", "__version__"]