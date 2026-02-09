"""
Constants and default patterns for TreeCatt
"""

# Patterns ignored by default
DEFAULT_IGNORE = {
    '.git', '.svn', '.hg', '.bzr',
    '.gitignore', '.gitattributes', '.gitmodules',

    '__pycache__', '*.pyc', '*.pyo', '*.pyd', '*.pyi',
    '.pytest_cache', '.mypy_cache', '.ruff_cache',
    '.coverage', 'coverage', 'htmlcov',
    '.tox', '.nox',

    'node_modules', '.npm', '.yarn', '.pnpm-store',
    'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml', 'uv.lock',

    'venv', 'env', '.venv', '.env', 'virtualenv',
    '.python-version',

    'dist', 'build', 'out', '.next', '.nuxt',
    '*.egg-info', '*.whl',

    '*.log', '*.tmp', '*.temp', '*.bak', '*.swp', '*.swo',

    '.DS_Store', 'Thumbs.db', 'desktop.ini',

    '.idea', '.vscode', '.fleet',

    'README', 'README.*',
    'LICENSE', 'LICENSE.*',
    'CHANGELOG.*', 'CONTRIBUTING.*', 'HISTORY.*',

    '*.md', '*.rst',

    '.classpath', '.project', '.settings',
    '.gradle', 'gradle-app.setting',
    '*.iml', '*.ipr', '*.iws',

    'target', '*.class', '*.jar', '*.war', '*.ear',

    '.cargo', 'target/debug', 'target/release',
    '*.rlib',

    'bin', 'obj', '*.dll', '*.exe', '*.pdb',

    'composer.lock', 'vendor',
    '*.phar',

    'Pods', '*.xcworkspace', '*.xcodeproj',
    'DerivedData', '*.ipa', '*.dSYM',

    '*.o', '*.a', '*.so', '*.dylib',
    '*.out',

    '.idea_modules', '.eslintcache', '.stylelintcache',
    '.cache', '.parcel-cache', '.turbo',

    '*.map', '*.min.js', '*.min.css',

    '.terraform', '*.tfstate', '*.tfstate.backup',
    '.terragrunt-cache',

    '.serverless', '.vercel', '.netlify',

    '.expo', '.expo-shared',

    '.angular', '.svelte-kit',

    '*.lock',

    '.gradle-cache', '.m2', '.ivy2',

    '.idea/**/workspace.xml',
    '.idea/**/tasks.xml',

    '.vagrant', '.docker', 'docker-compose.override.yml',

    '*.sqlite', '*.sqlite3', '*.db',

    '*.pem', '*.key', '*.crt',

    '*.pid',

    '*.orig', '*.rej',

    '*.coverage',

    '.bundle', 'Gemfile.lock',
    '.rvmrc', '.ruby-version',

    '.nuget', '*.nupkg',

    '.meteor', '.meteor/local',

    '*.tsbuildinfo',

    '.idea_modules', '.phpunit.result.cache',

    '.sass-cache', '*.scssc',

    '.pytest_cache',

    '.sonar', '.scannerwork',

    '.idea/**/dataSources',
    '.idea/**/dataSources.local.xml',

    '*.bak~', '*.old',

    '.idea/**/shelf',

    '*.tmp.*',

    '.cache-loader',

    '.gradle-wrapper',

    '.idea/**/httpRequests',

    '.idea/**/modules.xml',

    '*.snap',

    '.vscode-test',

    '.idea/**/misc.xml',

    '.idea/**/encodings.xml',

    '.idea/**/deployment.xml',

    '*.stackdump',

    '.idea/**/uiDesigner.xml'
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