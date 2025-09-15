#!/usr/bin/env python3
"""
Project Tree Generator
Generates a clean project tree structure ignoring unimportant folders and files.
"""

import os
import sys
from pathlib import Path

# Folders and files to ignore (case-insensitive)
IGNORE_PATTERNS = {
    # Version control
    '.git', '.gitignore', '.gitattributes',
    
    # Python
    '__pycache__', '*.pyc', '*.pyo', '*.pyd', '.Python',
    'build', 'develop-eggs', 'dist', 'downloads', 'eggs', '.eggs',
    'lib', 'lib64', 'parts', 'sdist', 'var', 'wheels', '*.egg-info',
    '.installed.cfg', '*.egg', 'MANIFEST',
    
    # Virtual environments
    'venv', 'env', '.venv', '.env', 'ENV', 'env.bak', 'venv.bak',
    
    # IDE and editors
    '.vscode', '.idea', '*.swp', '*.swo', '*~',
    '.DS_Store', 'Thumbs.db',
    
    # Dependencies
    'node_modules', 'bower_components',
    
    # Logs and temporary files
    '*.log', 'logs', '.npm', '.cache',
    
    # OS generated files
    '.DS_Store', '.DS_Store?', '._*', '.Spotlight-V100', '.Trashes',
    'ehthumbs.db', 'Thumbs.db',
    
    # Project specific (can be customized)
    '.pytest_cache', '.coverage', 'htmlcov',
    '*.sqlite', '*.db',
}

# File extensions to ignore
IGNORE_EXTENSIONS = {
    '.pyc', '.pyo', '.pyd', '.log', '.tmp', '.temp', '.swp', '.swo',
    '.db', '.sqlite', '.sqlite3'
}

def should_ignore(path_name: str) -> bool:
    """Check if a file or directory should be ignored."""
    path_name_lower = path_name.lower()
    
    # Check against ignore patterns
    for pattern in IGNORE_PATTERNS:
        if pattern.startswith('*'):
            # Handle wildcard patterns
            if path_name_lower.endswith(pattern[1:]):
                return True
        elif pattern == path_name_lower:
            return True
    
    # Check file extensions
    for ext in IGNORE_EXTENSIONS:
        if path_name_lower.endswith(ext):
            return True
    
    return False

def generate_tree(directory: Path, prefix: str = "", max_depth: int = None, current_depth: int = 0) -> None:
    """Generate and print the directory tree structure."""
    if max_depth is not None and current_depth >= max_depth:
        return
    
    try:
        # Get all items in directory, filter out ignored ones
        items = []
        for item in directory.iterdir():
            if not should_ignore(item.name):
                items.append(item)
        
        # Sort items: directories first, then files
        items.sort(key=lambda x: (x.is_file(), x.name.lower()))
        
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            
            # Choose the appropriate tree characters
            if is_last:
                current_prefix = "└── "
                next_prefix = prefix + "    "
            else:
                current_prefix = "├── "
                next_prefix = prefix + "│   "
            
            # Print current item
            if item.is_dir():
                print(f"{prefix}{current_prefix}{item.name}/")
                # Recursively process subdirectory
                generate_tree(item, next_prefix, max_depth, current_depth + 1)
            else:
                print(f"{prefix}{current_prefix}{item.name}")
                
    except PermissionError:
        print(f"{prefix}[Permission Denied]")

def main():
    """Main function to run the project tree generator."""
    # Get the project root directory (assuming script is in scripts/ folder)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Parse command line arguments
    max_depth = None
    if len(sys.argv) > 1:
        try:
            max_depth = int(sys.argv[1])
        except ValueError:
            print("Usage: python project_tree.py [max_depth]")
            print("max_depth: optional integer to limit tree depth")
            sys.exit(1)
    
    print(f"Project Tree for: {project_root.name}")
    print("=" * 50)
    print(f"{project_root.name}/")
    
    generate_tree(project_root, max_depth=max_depth)
    
    print("\n" + "=" * 50)
    print("Tree generation complete!")
    if max_depth:
        print(f"(Limited to depth: {max_depth})")

if __name__ == "__main__":
    main()
