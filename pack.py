#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Universal File Packer
Packs multiple files into a single template file with markers.
Respects .gitignore by default.

Usage:
    python pack.py [SOURCE_DIR] [OPTIONS]

Arguments:
    SOURCE_DIR              Source directory containing files to pack (default: ./ПАПКА)

Options:
    -h, --help              Show this help message
    -o, --output PATH       Output directory (default: ./output)
    -n, --name NAME         Output filename (default: DATA_compact.txt)
    -y, --yes               Answer yes to all prompts
    -v, --verbose           Verbose output
    -e, --exclude PATTERN   Exclude files matching pattern (can be used multiple times)
    -i, --include-ignored   Include files ignored by .gitignore
    -a, --include-all       Include all files (ignore .gitignore and default excludes)

Examples:
    python pack.py                           # Pack files from ./ПАПКА (respects .gitignore)
    python pack.py ./my_project              # Pack files from ./my_project
    python pack.py -i                        # Include .gitignore files
    python pack.py -a                        # Include ALL files
    python pack.py -e "*.pyc" -e "*.log"     # Additional excludes

Author: Виктор Макаров
Email: vmakarov.kzn@gmail.com
GitHub: @VikM78
"""

import os
import sys
import glob
import argparse
from pathlib import Path
from typing import List, Optional, Set, Dict, Tuple
import fnmatch

# Import configuration
from config import COMMENT_STYLES, SPECIAL_FILES, DEFAULT_EXCLUDES, get_comment_style

class Packer:
    """Main packer class with interactive and non-interactive modes."""
    
    def __init__(self):
        self.source_dir = None
        self.output_dir = None
        self.output_name = None
        self.exclude_patterns = []
        self.include_ignored = False
        self.include_all = False
        self.verbose = False
        self.auto_yes = False
        self.script_name = Path(sys.argv[0]).name
        self.gitignore_patterns = []
        
    def parse_arguments(self):
        """Parse command line arguments."""
        script_name = self.script_name
        
        parser = argparse.ArgumentParser(
            description="Universal File Packer - Pack files into a single template",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=f"""
Examples:
    python {script_name}                           # Pack files from ./ПАПКА (respects .gitignore)
    python {script_name} ./my_project              # Pack files from ./my_project
    python {script_name} -i                        # Include .gitignore files
    python {script_name} -a                        # Include ALL files
    python {script_name} -e "*.pyc" -e "*.log"     # Additional excludes
            """
        )
        
        parser.add_argument(
            'source_dir',
            nargs='?',
            default='./ПАПКА',
            help='Source directory containing files to pack (default: ./ПАПКА)'
        )
        
        parser.add_argument(
            '-o', '--output',
            dest='output_dir',
            default='./output',
            help='Output directory (default: ./output)'
        )
        
        parser.add_argument(
            '-n', '--name',
            dest='output_name',
            default='DATA_compact.txt',
            help='Output filename (default: DATA_compact.txt)'
        )
        
        parser.add_argument(
            '-e', '--exclude',
            dest='exclude_patterns',
            action='append',
            help='Exclude files matching pattern (can be used multiple times)'
        )
        
        parser.add_argument(
            '-i', '--include-ignored',
            action='store_true',
            help='Include files ignored by .gitignore'
        )
        
        parser.add_argument(
            '-a', '--include-all',
            action='store_true',
            help='Include ALL files (ignore .gitignore and default excludes)'
        )
        
        parser.add_argument(
            '-y', '--yes',
            action='store_true',
            help='Answer yes to all prompts'
        )
        
        parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='Verbose output'
        )
        
        return parser.parse_args()
    
    def load_gitignore(self, source_dir: Path) -> List[str]:
        """Load .gitignore patterns from source directory."""
        gitignore_path = source_dir / '.gitignore'
        patterns = []
        
        if gitignore_path.exists():
            try:
                with open(gitignore_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        # Skip empty lines and comments
                        if line and not line.startswith('#'):
                            patterns.append(line)
                if self.verbose:
                    print(f"  Loaded {len(patterns)} patterns from .gitignore")
            except Exception as e:
                if self.verbose:
                    print(f"  Warning: Could not read .gitignore: {e}")
        else:
            if self.verbose:
                print("  No .gitignore file found")
        
        return patterns
    
    def get_source_dir(self, args):
        """Get source directory from args or interactive prompt."""
        if args.source_dir:
            source_path = Path(args.source_dir)
            if source_path.exists() and source_path.is_dir():
                return source_path
        
        # Interactive prompt
        print("\n" + "="*60)
        print(" Universal File Packer")
        print("="*60)
        
        default_path = Path.cwd() / "ПАПКА"
        print(f"\nSource directory (default: {default_path}):")
        
        if self.auto_yes:
            return default_path
        
        while True:
            user_input = input("> ").strip()
            if not user_input:
                return default_path
            
            path = Path(user_input)
            if path.exists() and path.is_dir():
                return path
            else:
                print(f"Directory '{path}' does not exist or is not a directory. Please enter a valid path.")
    
    def get_output_path(self, args):
        """Get output path from args or interactive prompt."""
        if args.output_dir:
            return Path(args.output_dir)
        
        # Interactive prompt
        default_path = Path.cwd() / "output"
        print(f"\nOutput directory (default: {default_path}):")
        
        if self.auto_yes:
            return default_path
        
        while True:
            user_input = input("> ").strip()
            if not user_input:
                return default_path
            
            path = Path(user_input)
            if path.parent.exists() or path.parent == Path.cwd():
                return path
            else:
                print(f"Parent directory {path.parent} does not exist. Please enter a valid path.")
    
    def get_output_name(self, args):
        """Get output filename from args or interactive prompt."""
        if args.output_name:
            return args.output_name
        
        # Interactive prompt
        default_name = "DATA_compact.txt"
        print(f"\nOutput filename (default: {default_name}):")
        
        if self.auto_yes:
            return default_name
        
        user_input = input("> ").strip()
        if not user_input:
            return default_name
        return user_input
    
    def get_exclude_patterns(self, args):
        """Get exclude patterns from args."""
        patterns = []
        
        # Always exclude if not include-all
        if not self.include_all:
            # Add gitignore patterns
            if not self.include_ignored:
                patterns.extend(self.gitignore_patterns)
            
            # Add default excludes
            patterns.extend(DEFAULT_EXCLUDES)
        
        # Add user patterns
        if args.exclude_patterns:
            patterns.extend(args.exclude_patterns)
        
        return patterns
    
    def should_exclude(self, file_path: Path, exclude_patterns: List[str]) -> bool:
        """Check if file should be excluded based on patterns."""
        if not exclude_patterns:
            return False
        
        # Get relative path from source directory
        try:
            rel_path = str(file_path.relative_to(self.source_dir))
        except ValueError:
            rel_path = str(file_path)
        
        for pattern in exclude_patterns:
            # Check exact match
            if pattern == rel_path:
                return True
            
            # Check filename match
            if fnmatch.fnmatch(file_path.name, pattern):
                return True
            
            # Check relative path match
            if fnmatch.fnmatch(rel_path, pattern):
                return True
            
            # Check absolute path match
            if fnmatch.fnmatch(str(file_path), pattern):
                return True
            
            # Check if pattern is in path (for directory patterns)
            if pattern in str(file_path) or pattern in rel_path:
                return True
        
        return False
    
    def pack_files(self, source_dir: Path, exclude_patterns: List[str]) -> List[Dict]:
        """Pack files from source directory into a list of file info dicts."""
        packed_files = []
        files_processed = 0
        files_skipped = 0
        
        # Walk through source directory
        for root, dirs, files in os.walk(source_dir):
            root_path = Path(root)
            
            # Skip excluded directories (only if not include-all)
            if not self.include_all:
                dirs[:] = [d for d in dirs if not self.should_exclude(root_path / d, exclude_patterns)]
            
            for file in files:
                file_path = root_path / file
                
                # Skip excluded files
                if self.should_exclude(file_path, exclude_patterns):
                    if self.verbose:
                        print(f"  Skipping excluded: {file_path.relative_to(source_dir)}")
                    files_skipped += 1
                    continue
                
                # Get relative path from source directory
                relative_path = file_path.relative_to(source_dir)
                
                # Skip empty files
                try:
                    if file_path.stat().st_size == 0:
                        if self.verbose:
                            print(f"  Skipping empty: {relative_path}")
                        files_skipped += 1
                        continue
                except:
                    pass
                
                # Read file content
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except UnicodeDecodeError:
                    # Try with different encoding or skip binary files
                    try:
                        with open(file_path, 'r', encoding='latin-1') as f:
                            content = f.read()
                    except:
                        if self.verbose:
                            print(f"  Skipping binary file: {relative_path}")
                        files_skipped += 1
                        continue
                except Exception as e:
                    if self.verbose:
                        print(f"  Error reading {relative_path}: {e}")
                    files_skipped += 1
                    continue
                
                # Get comment style for the file using config
                start_comment, end_comment = get_comment_style(str(relative_path))
                
                # Add to packed files
                packed_files.append({
                    'path': str(relative_path),
                    'content': content,
                    'start_comment': start_comment,
                    'end_comment': end_comment,
                    'extension': Path(relative_path).suffix.lower(),
                    'filename': Path(relative_path).name
                })
                files_processed += 1
                
                if self.verbose:
                    print(f"  Packed: {relative_path} ({start_comment}style)")
        
        print(f"\nFiles processed: {files_processed}")
        print(f"Files skipped: {files_skipped}")
        
        return packed_files
    
    def create_template(self, packed_files: List[Dict], output_path: Path):
        """Create a single template file from packed files."""
        with open(output_path, 'w', encoding='utf-8') as f:
            # Write header
            f.write("# Universal File Packer - Generated Template\n")
            f.write(f"# Source: {self.source_dir}\n")
            f.write(f"# Files: {len(packed_files)}\n")
            f.write("#" + "="*58 + "\n\n")
            
            for file_info in packed_files:
                path = file_info['path']
                content = file_info['content']
                start_comment = file_info['start_comment']
                end_comment = file_info['end_comment']
                
                # Write start marker with appropriate comment style
                if start_comment:
                    f.write(f"{start_comment}start_my_file {path}\n")
                else:
                    f.write(f"start_my_file {path}\n")
                
                # Write content
                if content:
                    f.write(content)
                    if not content.endswith('\n'):
                        f.write('\n')
                
                # Write end marker with appropriate comment style
                if end_comment:
                    f.write(f"{end_comment}end_my_file {path}\n")
                else:
                    f.write(f"end_my_file {path}\n")
                
                # Add blank line between files
                f.write("\n")
    
    def run(self):
        """Main packing process."""
        args = self.parse_arguments()
        
        self.verbose = args.verbose
        self.auto_yes = args.yes
        self.include_ignored = args.include_ignored
        self.include_all = args.include_all
        
        print("="*60)
        print(f" Universal File Packer ({self.script_name})")
        print("="*60)
        if self.include_all:
            print(" Mode: INCLUDE ALL FILES")
        elif self.include_ignored:
            print(" Mode: INCLUDE .gitignore FILES")
        else:
            print(" Mode: RESPECT .gitignore")
        print(" Press Ctrl+C to cancel at any time")
        print("")
        
        try:
            # Get source directory
            self.source_dir = self.get_source_dir(args)
            print(f" Source directory: {self.source_dir}")
            
            # Get output directory
            self.output_dir = self.get_output_path(args)
            print(f" Output directory: {self.output_dir}")
            
            # Get output filename
            self.output_name = self.get_output_name(args)
            print(f" Output filename: {self.output_name}")
            
            # Load .gitignore
            if not self.include_all:
                self.gitignore_patterns = self.load_gitignore(self.source_dir)
                if self.verbose:
                    print(f" Gitignore patterns: {self.gitignore_patterns}")
            
            # Get exclude patterns
            self.exclude_patterns = self.get_exclude_patterns(args)
            if self.verbose:
                print(f" Exclude patterns: {self.exclude_patterns}")
            
            # Check if source directory exists
            if not self.source_dir.exists():
                print(f" Error: Source directory '{self.source_dir}' does not exist!")
                sys.exit(1)
            
            # Check if output directory exists and not empty
            if self.output_dir.exists():
                if any(self.output_dir.iterdir()):
                    print(f"Warning: {self.output_dir} already exists and is not empty.")
                    if not self.auto_yes:
                        response = input("Continue anyway? (y/N): ").strip().lower()
                        if response not in ('y', 'yes'):
                            print("Packing cancelled.")
                            return
            
            # Create output directory
            self.output_dir.mkdir(parents=True, exist_ok=True)
            
            # Pack files
            print("\n" + "="*60)
            print(" Packing Files")
            print("="*60)
            
            packed_files = self.pack_files(self.source_dir, self.exclude_patterns)
            
            if not packed_files:
                print(" No files found to pack!")
                print(" Check your source directory and exclude patterns.")
                sys.exit(1)
            
            # Create template
            output_path = self.output_dir / self.output_name
            self.create_template(packed_files, output_path)
            
            print("\n" + "="*60)
            print(" Packing completed successfully!")
            print(f" Output file: {output_path}")
            print(f" Files packed: {len(packed_files)}")
            print("="*60)
            
            # Show next steps
            print("\n Next steps:")
            print(f"   1. Check the generated template: {output_path}")
            print("   2. Use extract.py to unpack files")
            print(f"   3. python extract.py {output_path.name} -o ./extracted")
            
        except KeyboardInterrupt:
            print("\n\n Packing cancelled by user.")
            sys.exit(1)
        except Exception as e:
            print(f"\n Error: {e}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            sys.exit(1)

def main():
    packer = Packer()
    packer.run()

if __name__ == "__main__":
    main()
