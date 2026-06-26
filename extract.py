#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Universal installer for DCIM_monitor project.
Creates folder structure and files from template text file.

Usage:
    python {script_name} [SOURCE_FILE] [OPTIONS]

Arguments:
    SOURCE_FILE             Source template file (default: текст_всех_файлов.txt)

Options:
    -h, --help              Show this help message
    -i, --install PATH      Installation directory (default: ./DCIM_monitor)
    -y, --yes               Answer yes to all prompts
    -v, --verbose           Verbose output

Examples:
    python {script_name}                         # Use default template
    python {script_name} DATA1.txt               # Use specific file
    python {script_name} DATA_01.txt -i /opt/proj # Use custom file and path
    python {script_name} -i /opt/myproject -y    # Non-interactive mode
"""

import os
import sys
import glob
import argparse
from pathlib import Path
from typing import List, Dict, Optional

class Installer:
    """Main installer class with interactive and non-interactive modes."""
    
    def __init__(self):
        self.project_dir = None
        self.source_files = []
        self.verbose = False
        self.auto_yes = False
        self.script_name = Path(sys.argv[0]).name
        
    def parse_arguments(self):
        """Parse command line arguments."""
        # Get script name for help text
        script_name = self.script_name
        
        parser = argparse.ArgumentParser(
            description="Universal installer for DCIM_monitor project",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=f"""
Examples:
    python {script_name}                         # Use default template
    python {script_name} DATA1.txt               # Use specific file
    python {script_name} DATA_01.txt -i /opt/proj # Use custom file and path
    python {script_name} -i /opt/myproject -y    # Non-interactive mode
            """
        )
        
        # Positional argument for source file
        parser.add_argument(
            'source_file',
            nargs='?',
            default='текст_всех_файлов.txt',
            help='Source template file (default: текст_всех_файлов.txt)'
        )
        
        parser.add_argument(
            '-i', '--install',
            dest='install_dir',
            help='Installation directory (default: ./DCIM_monitor)'
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
    
    def get_install_path(self, args):
        """Get installation path from args or interactive prompt."""
        if args.install_dir:
            return Path(args.install_dir)
        
        # Interactive prompt
        print("\n" + "="*60)
        print(" DCIM_monitor Installer")
        print("="*60)
        
        default_path = Path.cwd() / "DCIM_monitor"
        print(f"\nInstallation directory (default: {default_path}):")
        
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
        
        # Try with DATA pattern
        if 'DATA' in args.source_file or '*' in args.source_file:
            # Try glob pattern
            matches = glob.glob(args.source_file)
            if matches:
                return [Path(f) for f in sorted(matches)]
            
            # Try with DATA* pattern
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
        
        # Look for DATA files in current directory
        data_files = sorted(glob.glob("DATA*"))
        if data_files:
            print("\nFound data files:")
            for i, f in enumerate(data_files, 1):
                print(f"  {i}. {f}")
            
            if not self.auto_yes:
                choice = input("\nUse all DATA files? (Y/n): ").strip().lower()
                if choice in ('', 'y', 'yes'):
                    return [Path(f) for f in data_files]
        
        # Manual input
        print("\nEnter source file(s) or directory:")
        print("  - Single file: template.txt")
        print("  - Directory: ./templates")
        print("  - Multiple files: DATA1.txt DATA2.txt")
        print("  - Pattern: DATA_*.txt")
        
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
                        # Search for DATA* files in directory
                        pattern = path / "DATA*"
                        dir_files = glob.glob(str(pattern))
                        if dir_files:
                            source_files.extend([Path(f) for f in sorted(dir_files)])
                        else:
                            print(f"No DATA* files found in {path}")
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
    
    def parse_template_file(self, file_path: Path) -> List[Dict]:
        """Parse a single template file with start_my_file/end_my_file markers."""
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
            line = lines[i].strip()
            
            if line.startswith("start_my_file "):
                filename = line.replace("start_my_file ", "").strip()
                i += 1
                
                content_lines = []
                while i < len(lines):
                    if lines[i].strip().startswith("end_my_file "):
                        end_filename = lines[i].strip().replace("end_my_file ", "").strip()
                        if end_filename == filename:
                            i += 1
                            break
                        else:
                            content_lines.append(lines[i])
                            i += 1
                    else:
                        content_lines.append(lines[i])
                        i += 1
                
                if filename and content_lines:
                    blocks.append({
                        "filename": filename,
                        "content": "\n".join(content_lines)
                    })
            else:
                i += 1
        
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
                # Check if file is a simple script without markers
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    # Use filename as the target filename
                    filename = file_path.name
                    if filename.endswith('.txt'):
                        filename = filename[:-4]
                    all_blocks.append({
                        "filename": filename,
                        "content": content
                    })
                    if self.verbose:
                        print(f"  Added as single file: {filename}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
        
        return all_blocks
    
    def create_project(self, blocks: List[Dict]):
        """Create project folders and files from blocks."""
        print("\n" + "="*60)
        print(" Installing DCIM_monitor Project")
        print("="*60)
        print(f" Target directory: {self.project_dir}")
        print(f" Source files: {len(blocks)} file blocks")
        print("")
        
        # Check if directory exists and not empty
        if self.project_dir.exists():
            if any(self.project_dir.iterdir()):
                print(f"Warning: {self.project_dir} already exists and is not empty.")
                if not self.auto_yes:
                    response = input("Continue anyway? (y/N): ").strip().lower()
                    if response not in ('y', 'yes'):
                        print("Installation cancelled.")
                        return
        
        # Create directory
        self.project_dir.mkdir(parents=True, exist_ok=True)
        
        created_files = 0
        created_dirs = set()
        
        for block in blocks:
            filename = block["filename"]
            content = block["content"]
            
            if not filename or not content.strip():
                if self.verbose:
                    print(f" Skipping empty: {filename}")
                continue
            
            file_path = self.project_dir / filename
            parent_dir = file_path.parent
            
            if not parent_dir.exists():
                parent_dir.mkdir(parents=True, exist_ok=True)
                created_dirs.add(str(parent_dir))
                if self.verbose:
                    print(f" Created directory: {parent_dir}")
            
            # Write file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            created_files += 1
            print(f" Created: {filename}")
        
        print("")
        print(f" Files created: {created_files}")
        print(f" Folders created: {len(created_dirs)}")
        print("")
        print("="*60)
        print(" Project successfully deployed!")
        print(f" Path: {self.project_dir}")
        print("="*60)
        print("")
        print(" Next steps:")
        print(f"   1. cd {self.project_dir}")
        print("   2. pip install -r requirements.txt")
        print("   3. cp .env.example .secrets/.env")
        print("   4. Edit .secrets/.env")
        print("   5. python run.py -a")
        print("")
    
    def run(self):
        """Main installation process."""
        args = self.parse_arguments()
        
        self.verbose = args.verbose
        self.auto_yes = args.yes
        
        print("="*60)
        print(f" DCIM_monitor Universal Installer ({self.script_name})")
        print("="*60)
        print(" Press Ctrl+C to cancel at any time")
        print("")
        
        try:
            # Get installation path
            self.project_dir = self.get_install_path(args)
            print(f" Installation directory: {self.project_dir}")
            
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
                print(" Make sure files contain 'start_my_file' and 'end_my_file' markers.")
                sys.exit(1)
            
            # Create project
            self.create_project(all_blocks)
            
        except KeyboardInterrupt:
            print("\n\n Installation cancelled by user.")
            sys.exit(1)
        except Exception as e:
            print(f"\n Error: {e}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            sys.exit(1)

def main():
    installer = Installer()
    installer.run()

if __name__ == "__main__":
    main()
