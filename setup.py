"""
Alternative setup for compatibility
"""
from setuptools import setup, find_packages

setup(
    name            = "treecatt",
    version         = "0.1.0",
    package_dir     = {"": "src"},
    packages        = find_packages(where="src"),
    python_requires = ">=3.8",
    entry_points    = {
        "console_scripts": [
            "treecatt=treecatt.main:main"
        ]
    },
)
