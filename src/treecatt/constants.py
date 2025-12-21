"""
Constants and default patterns for TreeCatt
"""

# Patterns ignored by default
DEFAULT_IGNORE = {
    'node_modules', '__pycache__', '.git', '.svn', '.hg',
    'venv', 'env', '.venv', 'virtualenv',
    '*.pyc', '*.pyo', '*.pyd', '.DS_Store',
    '*.log', '*.tmp', '*.temp',
    'dist', 'build', '.pytest_cache', '.mypy_cache',
    'coverage', '.coverage', 'htmlcov',
    '.idea', '.vscode', '*.swp', '*.swo',
    'README.md', 'README.rst', 'README.txt', 'README',
    'LICENSE', 'LICENSE.txt', 'LICENSE.md',
    'CHANGELOG.md', 'CONTRIBUTING.md', 'HISTORY.md',
    '*.md', '*.rst'
}

# Sensitive files ignored by default
SENSITIVE_FILES = {
    '.env', '.env.local', '.env.production', 
    '*.pem', '*.key', 'id_rsa', 'id_dsa'
}

# Known binary extensions to exclude (more efficient than testing each file)
BINARY_EXTENSIONS = {
    # Images
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.svg', '.webp', '.tiff', '.psd',
    # Videos
    '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg',
    # Audio
    '.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', '.opus',
    # Archives
    '.zip', '.tar', '.gz', '.bz2', '.xz', '.7z', '.rar', '.iso',
    # Executables
    '.exe', '.dll', '.so', '.dylib', '.bin', '.app',
    # Binary documents
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.odt', '.ods',
    # Databases
    '.db', '.sqlite', '.sqlite3', '.mdb',
    # Compiled
    '.pyc', '.pyo', '.pyd', '.class', '.o', '.obj', '.a', '.lib',
    # Fonts
    '.ttf', '.otf', '.woff', '.woff2', '.eot',
    # Other
    '.swf', '.jar', '.war', '.ear'
}