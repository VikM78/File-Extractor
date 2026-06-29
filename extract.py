#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Universal File Extractor
Extracts files from template text files with support for ANY comment styles.

Usage:
    python extract.py [SOURCE_FILE] [OPTIONS]

Arguments:
    SOURCE_FILE             Source template file (default: template.txt)

Options:
    -h, --help              Show this help message
    -o, --output PATH       Output directory (default: ./extracted_files)
    -y, --yes               Answer yes to all prompts
    -v, --verbose           Verbose output

Examples:
    python extract.py                         # Use default template
    python extract.py DATA1.txt               # Use specific file
    python extract.py template.txt -o ./output # Custom output directory
    python extract.py -o ./project -y         # Non-interactive mode

Author: Виктор Макаров
Email: vmakarov.kzn@gmail.com
GitHub: @VikM78
"""

import os
import sys
import glob
import re
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Pattern

# Import configuration
from config import EXTRACT_PATTERNS

class Extractor:
    """Main extractor class with support for unlimited comment styles."""
    
    def __init__(self):
        self.output_dir = None
        self.source_files = []
        self.verbose = False
        self.auto_yes = False
        self.script_name = Path(sys.argv[0]).name
        # Компилируем все паттерны заранее для производительности
        self.start_patterns = []
        self.end_patterns = []
        for start_re, end_re, style_name in EXTRACT_PATTERNS:
            self.start_patterns.append((re.compile(start_re), style_name))
            self.end_patterns.append((re.compile(end_re), style_name))
        
    def parse_arguments(self):
        """Parse command line arguments."""
        script_name = self.script_name
        
        parser = argparse.ArgumentParser(
            description="Universal File Extractor - Extract files from templates",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=f"""
Examples:
    python {script_name}                         # Use default template
    python {script_name} DATA1.txt               # Use specific file
    python {script_name} template.txt -o ./output # Custom output directory
    python {script_name} -o ./project -y         # Non-interactive mode
            """
        )
        
        parser.add_argument(
            'source_file',
            nargs='?',
            default='template.txt',
            help='Source template file (default: template.txt)'
        )
        
        parser.add_argument(
            '-o', '--output',
            dest='output_dir',
            help='Output directory (default: ./extracted_files)'
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
    
    def get_output_path(self, args):
        """Get output path from args or interactive prompt."""
        if args.output_dir:
            return Path(args.output_dir)
        
        # Interactive prompt
        print("\n" + "="*60)
        print(" Universal File Extractor")
        print("="*60)
        
        default_path = Path.cwd() / "extracted_files"
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
    
    def get_source_files(self, args):
        """Get source files based on arguments."""
        source_path = Path(args.source_file)
        
        # If file exists, use it
        if source_path.exists() and source_path.is_file():
            return [source_path]
        
        # Try with pattern
        if '*' in args.source_file or '?' in args.source_file:
            matches = glob.glob(args.source_file)
            if matches:
                return [Path(f) for f in sorted(matches)]
        
        # Try with DATA pattern
        if 'DATA' in args.source_file:
            data_files = sorted(glob.glob("DATA*"))
            if data_files:
                print(f"\nFile '{args.source_file}' not found. Found DATA files:")
                for i, f in enumerate(data_files, 1):
                    print(f"  {i}. {f}")
                
                if not self.auto_yes:
                    choice = input("\nUse all DATA files? (Y/n): ").strip().lower()
                    if choice in ('', 'y', 'yes'):
                        return [Path(f) for f in data_files]
        
        # File not found - interactive mode
        print(f"\nFile '{args.source_file}' not found.")
        
        # Look for template files in current directory
        template_files = sorted(glob.glob("*.txt"))
        if template_files:
            print("\nFound template files:")
            for i, f in enumerate(template_files, 1):
                print(f"  {i}. {f}")
            
            if not self.auto_yes:
                choice = input("\nUse all template files? (Y/n): ").strip().lower()
                if choice in ('', 'y', 'yes'):
                    return [Path(f) for f in template_files]
        
        # Manual input
        print("\nEnter source file(s) or directory:")
        print("  - Single file: template.txt")
        print("  - Directory: ./templates")
        print("  - Multiple files: file1.txt file2.txt")
        print("  - Pattern: *.txt")
        
        if self.auto_yes:
            print("No source files specified. Exiting.")
            sys.exit(1)
        
        source_files = []
        while True:
            user_input = input("> ").strip()
            if not user_input:
                print("Please enter at least one source.")
                continue
            
            # Parse input
            parts = user_input.split()
            for part in parts:
                path = Path(part)
                if path.exists():
                    if path.is_file():
                        source_files.append(path)
                    elif path.is_dir():
                        # Search for template files in directory
                        pattern = path / "*.txt"
                        dir_files = glob.glob(str(pattern))
                        if dir_files:
                            source_files.extend([Path(f) for f in sorted(dir_files)])
                        else:
                            print(f"No template files found in {path}")
                    else:
                        print(f"Path does not exist: {path}")
                else:
                    # Try with glob pattern
                    matches = glob.glob(part)
                    if matches:
                        source_files.extend([Path(f) for f in sorted(matches)])
                    else:
                        print(f"No files matching: {part}")
            
            if source_files:
                break
            else:
                print("No valid sources found. Try again.")
        
        return source_files
    
    def find_matching_pattern(self, line: str, patterns: List) -> Optional[Tuple[Pattern, str, str]]:
        """Find matching pattern for a line."""
        for pattern, style_name in patterns:
            match = pattern.match(line)
            if match:
                return match, pattern, style_name
        return None, None, None
    
    def parse_template_file(self, file_path: Path) -> List[Dict]:
        """Parse a single template file with support for unlimited comment styles."""
        blocks = []
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return blocks
        
        lines = content.splitlines()
        
        i = 0
        while i < len(lines):
            line = lines[i]
            matched = False
            
            # Проверяем все start паттерны
            start_result = self.find_matching_pattern(line, self.start_patterns)
            if start_result[0] is not None:
                match, start_pattern, start_style = start_result
                filename = match.group(1).strip()
                i += 1
                
                content_lines = []
                found_end = False
                
                # Ищем end маркер любым из паттернов
                while i < len(lines):
                    end_result = self.find_matching_pattern(lines[i], self.end_patterns)
                    if end_result[0] is not None:
                        end_match, end_pattern, end_style = end_result
                        end_filename = end_match.group(1).strip()
                        if end_filename == filename:
                            found_end = True
                            i += 1
                            break
                        else:
                            # Неправильный end маркер - добавляем как контент
                            content_lines.append(lines[i])
                            i += 1
                    else:
                        content_lines.append(lines[i])
                        i += 1
                
                if filename and content_lines:
                    blocks.append({
                        "filename": filename,
                        "content": "\n".join(content_lines),
                        "start_style": start_style,
                        "end_style": end_style if found_end else "not_found"
                    })
                    if self.verbose:
                        print(f"  Found block: {filename} (style: {start_style})")
                
                matched = True
            
            if not matched:
                i += 1
        
        # Если блоки не найдены, пробуем обработать как один файл
        if not blocks:
            filename = file_path.name
            if filename.endswith('.txt'):
                filename = filename[:-4]
            blocks.append({
                "filename": filename,
                "content": content,
                "start_style": "single_file",
                "end_style": "single_file"
            })
            if self.verbose:
                print(f"  No markers found, treating as single file: {filename}")
        
        return blocks
    
    def parse_multiple_files(self, file_paths: List[Path]) -> List[Dict]:
        """Parse multiple source files."""
        all_blocks = []
        
        for file_path in file_paths:
            if self.verbose:
                print(f"Processing: {file_path}")
            
            blocks = self.parse_template_file(file_path)
            if blocks:
                if self.verbose:
                    print(f"  Found {len(blocks)} file blocks in {file_path.name}")
                all_blocks.extend(blocks)
            else:
                print(f"  No blocks found in {file_path}")
        
        return all_blocks
    
    def extract_files(self, blocks: List[Dict]):
        """Extract files to output directory."""
        print("\n" + "="*60)
        print(" Extracting Files")
        print("="*60)
        print(f" Output directory: {self.output_dir}")
        print(f" Files to extract: {len(blocks)}")
        print("")
        
        # Check if directory exists and not empty
        if self.output_dir.exists():
            if any(self.output_dir.iterdir()):
                print(f"Warning: {self.output_dir} already exists and is not empty.")
                if not self.auto_yes:
                    response = input("Continue anyway? (y/N): ").strip().lower()
                    if response not in ('y', 'yes'):
                        print("Extraction cancelled.")
                        return
        
        # Create directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        extracted_files = 0
        created_dirs = set()
        
        for block in blocks:
            filename = block["filename"]
            content = block["content"]
            
            if not filename or not content.strip():
                if self.verbose:
                    print(f" Skipping empty: {filename}")
                continue
            
            file_path = self.output_dir / filename
            parent_dir = file_path.parent
            
            if not parent_dir.exists():
                parent_dir.mkdir(parents=True, exist_ok=True)
                created_dirs.add(str(parent_dir))
                if self.verbose:
                    print(f" Created directory: {parent_dir}")
            
            # Write file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            extracted_files += 1
            print(f" Extracted: {filename}")
        
        print("")
        print(f" Files extracted: {extracted_files}")
        print(f" Folders created: {len(created_dirs)}")
        print("")
        print("="*60)
        print(" Extraction completed successfully!")
        print(f" Output path: {self.output_dir}")
        print("="*60)
    
    def run(self):
        """Main extraction process."""
        args = self.parse_arguments()
        
        self.verbose = args.verbose
        self.auto_yes = args.yes
        
        print("="*60)
        print(f" Universal File Extractor ({self.script_name})")
        print("="*60)
        print(" Press Ctrl+C to cancel at any time")
        print("")
        
        try:
            # Get output path
            self.output_dir = self.get_output_path(args)
            print(f" Output directory: {self.output_dir}")
            
            # Get source files
            self.source_files = self.get_source_files(args)
            print(f" Source files: {len(self.source_files)}")
            if self.verbose:
                for f in self.source_files:
                    print(f"  - {f}")
            
            # Parse source files
            all_blocks = self.parse_multiple_files(self.source_files)
            
            if not all_blocks:
                print(" No file blocks found in source files!")
                print(" Make sure files contain markers with comments.")
                sys.exit(1)
            
            # Extract files
            self.extract_files(all_blocks)
            
        except KeyboardInterrupt:
            print("\n\n Extraction cancelled by user.")
            sys.exit(1)
        except Exception as e:
            print(f"\n Error: {e}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            sys.exit(1)

def main():
    extractor = Extractor()
    extractor.run()

if __name__ == "__main__":
    main()
