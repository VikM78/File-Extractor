#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration file for Universal File Extractor & Packer
Contains comment styles for different file types.
"""

# Расширенная карта стилей комментариев для разных типов файлов
COMMENT_STYLES = {
    # Языки программирования
    '.py': ('# ', '# '),           # Python
    '.pyw': ('# ', '# '),          # Python Windows
    '.sh': ('# ', '# '),           # Shell
    '.bash': ('# ', '# '),         # Bash
    '.zsh': ('# ', '# '),          # Zsh
    '.fish': ('# ', '# '),         # Fish
    '.rb': ('# ', '# '),           # Ruby
    '.rbw': ('# ', '# '),          # Ruby Windows
    '.pl': ('# ', '# '),           # Perl
    '.pm': ('# ', '# '),           # Perl Module
    '.t': ('# ', '# '),            # Perl Test
    '.go': ('// ', '// '),         # Go
    '.rs': ('// ', '// '),         # Rust
    '.swift': ('// ', '// '),      # Swift
    '.java': ('// ', '// '),       # Java
    '.kt': ('// ', '// '),         # Kotlin
    '.kts': ('// ', '// '),        # Kotlin Script
    '.c': ('// ', '// '),          # C
    '.cpp': ('// ', '// '),        # C++
    '.cc': ('// ', '// '),         # C++
    '.cxx': ('// ', '// '),        # C++
    '.h': ('// ', '// '),          # C/C++ Header
    '.hpp': ('// ', '// '),        # C++ Header
    '.hxx': ('// ', '// '),        # C++ Header
    '.js': ('// ', '// '),         # JavaScript
    '.jsx': ('// ', '// '),        # React JSX
    '.mjs': ('// ', '// '),        # ES Module
    '.ts': ('// ', '// '),         # TypeScript
    '.tsx': ('// ', '// '),        # React TSX
    '.php': ('// ', '// '),        # PHP
    '.phtml': ('// ', '// '),      # PHP HTML
    '.lua': ('-- ', '-- '),        # Lua
    '.hs': ('{- ', ' -}'),         # Haskell
    '.lhs': ('{- ', ' -}'),        # Literate Haskell
    '.elm': ('{- ', ' -}'),        # Elm
    '.ml': ('(* ', ' *)'),         # OCaml
    '.mli': ('(* ', ' *)'),        # OCaml Interface
    '.scala': ('// ', '// '),      # Scala
    '.clj': ('; ', '; '),          # Clojure
    '.cljs': ('; ', '; '),         # ClojureScript
    '.dart': ('// ', '// '),       # Dart
    '.r': ('# ', '# '),            # R
    '.rmd': ('<!-- ', ' -->'),     # R Markdown
    '.jl': ('# ', '# '),           # Julia
    '.ex': ('# ', '# '),           # Elixir
    '.exs': ('# ', '# '),          # Elixir Script
    '.erl': ('% ', '% '),          # Erlang
    '.hrl': ('% ', '% '),          # Erlang Header
    '.fs': ('// ', '// '),         # F#
    '.fsi': ('// ', '// '),        # F# Interface
    '.fsx': ('// ', '// '),        # F# Script
    '.vb': ("' ", "' "),           # Visual Basic
    '.vbs': ("' ", "' "),          # VBScript
    '.ps1': ('# ', '# '),          # PowerShell
    '.psm1': ('# ', '# '),         # PowerShell Module
    '.psd1': ('# ', '# '),         # PowerShell Data
    
    # Веб-технологии
    '.html': ('<!-- ', ' -->'),    # HTML
    '.htm': ('<!-- ', ' -->'),     # HTML
    '.xhtml': ('<!-- ', ' -->'),   # XHTML
    '.xml': ('<!-- ', ' -->'),     # XML
    '.svg': ('<!-- ', ' -->'),     # SVG
    '.vue': ('<!-- ', ' -->'),     # Vue.js
    '.svelte': ('<!-- ', ' -->'),  # Svelte
    '.erb': ('<%# ', ' %>'),       # ERB (Ruby)
    '.ejs': ('<%# ', ' %>'),       # EJS (JavaScript)
    '.hbs': ('{{! ', ' }}'),       # Handlebars
    '.mustache': ('{{! ', ' }}'),  # Mustache
    
    # Стили
    '.css': ('/* ', ' */'),        # CSS
    '.scss': ('/* ', ' */'),       # SCSS
    '.sass': ('// ', '// '),       # SASS
    '.less': ('// ', '// '),       # LESS
    '.styl': ('// ', '// '),       # Stylus
    '.pcss': ('/* ', ' */'),       # PostCSS
    '.sss': ('// ', '// '),        # SugarSS
    
    # Конфигурационные файлы
    '.ini': ('; ', '; '),          # INI
    '.cfg': ('# ', '# '),          # Config
    '.conf': ('# ', '# '),         # Config
    '.yml': ('# ', '# '),          # YAML
    '.yaml': ('# ', '# '),         # YAML
    '.toml': ('# ', '# '),         # TOML
    '.json': ('// ', '// '),       # JSON (для совместимости)
    '.json5': ('// ', '// '),      # JSON5
    '.hjson': ('# ', '# '),        # HJSON
    '.env': ('# ', '# '),          # Environment
    '.properties': ('# ', '# '),   # Java Properties
    '.prop': ('# ', '# '),         # Properties
    '.xaml': ('<!-- ', ' -->'),    # XAML
    
    # Базы данных
    '.sql': ('-- ', '-- '),        # SQL
    '.psql': ('-- ', '-- '),       # PostgreSQL
    '.mysql': ('-- ', '-- '),      # MySQL
    '.sqlite': ('-- ', '-- '),     # SQLite
    '.plsql': ('-- ', '-- '),      # PL/SQL
    '.pgsql': ('-- ', '-- '),      # PostgreSQL
    '.tsql': ('-- ', '-- '),       # T-SQL
    
    # Документация
    '.md': ('<!-- ', ' -->'),      # Markdown
    '.markdown': ('<!-- ', ' -->'),# Markdown
    '.rst': ('.. ', '.. '),        # reStructuredText
    '.txt': ('# ', '# '),          # Plain text
    '.text': ('# ', '# '),         # Plain text
    '.adoc': ('// ', '// '),       # AsciiDoc
    '.asciidoc': ('// ', '// '),   # AsciiDoc
    '.org': ('# ', '# '),          # Org-mode
    '.tex': ('% ', '% '),          # LaTeX
    '.latex': ('% ', '% '),        # LaTeX
    
    # Другие
    '.dockerfile': ('# ', '# '),   # Dockerfile
    'dockerfile': ('# ', '# '),    # Dockerfile
    '.makefile': ('# ', '# '),     # Makefile
    'makefile': ('# ', '# '),      # Makefile
    '.mk': ('# ', '# '),           # Makefile
    '.cmake': ('# ', '# '),        # CMake
    '.cmake.in': ('# ', '# '),     # CMake Input
    '.ninja': ('# ', '# '),        # Ninja
    '.gradle': ('// ', '// '),     # Gradle
    '.groovy': ('// ', '// '),     # Groovy
    '.jenkinsfile': ('// ', '// '),# Jenkinsfile
    '.tf': ('# ', '# '),           # Terraform
    '.tfvars': ('# ', '# '),       # Terraform Variables
    '.hcl': ('# ', '# '),          # HCL
    '.nomad': ('# ', '# '),        # Nomad
    '.vault': ('# ', '# '),        # Vault
    '.proto': ('// ', '// '),      # Protocol Buffers
    '.thrift': ('// ', '// '),     # Thrift
    '.avsc': ('// ', '// '),       # Avro Schema
    '.graphql': ('# ', '# '),      # GraphQL
    '.gql': ('# ', '# '),          # GraphQL
    '.cql': ('-- ', '-- '),        # Cassandra CQL
    
    # Системные
    '.bat': (':: ', ':: '),        # Batch
    '.cmd': (':: ', ':: '),        # Command
    '.vbe': ("' ", "' "),          # VBScript Encoded
    '.wsf': ('<!-- ', ' -->'),     # Windows Script File
    '.wsh': ('<!-- ', ' -->'),     # Windows Script Host
    
    # Специальные
    '.gitignore': ('# ', '# '),    # Git Ignore
    '.gitattributes': ('# ', '# '),# Git Attributes
    '.gitmodules': ('# ', '# '),   # Git Modules
    '.editorconfig': ('# ', '# '), # EditorConfig
    '.eslintrc': ('// ', '// '),   # ESLint
    '.prettierrc': ('// ', '// '), # Prettier
    '.stylelintrc': ('// ', '// '),# Stylelint
    '.babelrc': ('// ', '// '),    # Babel
    '.npmrc': ('# ', '# '),        # npm
    '.yarnrc': ('# ', '# '),       # yarn
    
    # По умолчанию
    'default': ('# ', '# '),       # Default
}

# Паттерны для распознавания маркеров в extract.py
# (start_pattern, end_pattern, style_name)
EXTRACT_PATTERNS = [
    # Без комментариев
    (r'^\s*start_my_file\s+(.+)$', r'^\s*end_my_file\s+(.+)$', 'plain'),
    
    # Python/Shell (# )
    (r'^\s*#\s*start_my_file\s+(.+)$', r'^\s*#\s*end_my_file\s+(.+)$', 'hash'),
    
    # C/Java/JS (// )
    (r'^\s*//\s*start_my_file\s+(.+)$', r'^\s*//\s*end_my_file\s+(.+)$', 'slash'),
    
    # HTML (<!-- -->) - на одной строке
    (r'^\s*<!--\s*start_my_file\s+(.+?)\s*-->$', r'^\s*<!--\s*end_my_file\s+(.+?)\s*-->$', 'html_single'),
    
    # HTML (<!-- -->) - на нескольких строках
    (r'^\s*<!--\s*start_my_file\s+(.+)$', r'^\s*<!--\s*end_my_file\s+(.+?)\s*-->$', 'html_multi'),
    
    # CSS (/* */)
    (r'^\s*/\*\s*start_my_file\s+(.+?)\s*\*/$', r'^\s*/\*\s*end_my_file\s+(.+?)\s*\*/$', 'css'),
    
    # SQL (-- )
    (r'^\s*--\s*start_my_file\s+(.+)$', r'^\s*--\s*end_my_file\s+(.+)$', 'sql'),
    
    # INI (; )
    (r'^\s*;\s*start_my_file\s+(.+)$', r'^\s*;\s*end_my_file\s+(.+)$', 'ini'),
    
    # Ruby/Perl (% )
    (r'^\s*%\s*start_my_file\s+(.+)$', r'^\s*%\s*end_my_file\s+(.+)$', 'percent'),
    
    # Pascal/Delphi ({ })
    (r'^\s*\{\s*start_my_file\s+(.+)\s*\}$', r'^\s*\{\s*end_my_file\s+(.+)\s*\}$', 'braces'),
    
    # Lua (--[[ ]])
    (r'^\s*--\[\[\s*start_my_file\s+(.+)\s*\]\]$', r'^\s*--\[\[\s*end_my_file\s+(.+)\s*\]\]$', 'lua'),
    
    # Haskell ({- -})
    (r'^\s*\{-\s*start_my_file\s+(.+)\s*-\}$', r'^\s*\{-\s*end_my_file\s+(.+)\s*-\}$', 'haskell'),
    
    # TeX/LaTeX (% )
    (r'^\s*%\s*start_my_file\s+(.+)$', r'^\s*%\s*end_my_file\s+(.+)$', 'tex'),
    
    # VHDL (-- )
    (r'^\s*--\s*start_my_file\s+(.+)$', r'^\s*--\s*end_my_file\s+(.+)$', 'vhdl'),
]

# Специальные файлы без расширения
SPECIAL_FILES = {
    'dockerfile': ('# ', '# '),
    'makefile': ('# ', '# '),
    'cmakelists.txt': ('# ', '# '),
    'jenkinsfile': ('// ', '// '),
    'vagrantfile': ('# ', '# '),
    'rakefile': ('# ', '# '),
    'gemfile': ('# ', '# '),
    'procfile': ('# ', '# '),
    'pom.xml': ('<!-- ', ' -->'),
    'web.config': ('<!-- ', ' -->'),
    'app.config': ('<!-- ', ' -->'),
    '.env': ('# ', '# '),
    '.gitignore': ('# ', '# '),
    '.gitattributes': ('# ', '# '),
    '.gitmodules': ('# ', '# '),
    '.editorconfig': ('# ', '# '),
    '.eslintrc': ('// ', '// '),
    '.prettierrc': ('// ', '// '),
    '.stylelintrc': ('// ', '// '),
    '.babelrc': ('// ', '// '),
    '.npmrc': ('# ', '# '),
    '.yarnrc': ('# ', '# '),
}

# Исключаемые по умолчанию паттерны
DEFAULT_EXCLUDES = [
    "*.pyc",
    "__pycache__",
    "*.log",
    "*.tmp",
    "*.bak",
    ".git",
    ".svn",
    ".DS_Store",
    "Thumbs.db",
    "*.swp",
    "*.swo",
    "*~"
]

def get_comment_style(file_path: str) -> tuple:
    """Get comment style based on file path and extension."""
    from pathlib import Path
    path_obj = Path(file_path)
    filename = path_obj.name.lower()
    ext = path_obj.suffix.lower()
    
    # Проверяем специальные файлы
    if filename in SPECIAL_FILES:
        return SPECIAL_FILES[filename]
    
    # Проверяем по расширению
    if ext in COMMENT_STYLES:
        return COMMENT_STYLES[ext]
    
    # По умолчанию
    return COMMENT_STYLES['default']
