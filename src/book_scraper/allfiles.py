#!/usr/bin/env python3
"""
Collect all Python files in a directory tree and combine them into a single file
with clear headers showing file paths.
"""

import os
import sys
from pathlib import Path

def collect_python_files(root_dir="."):
    """Collect all Python files in the directory tree."""
    python_files = []
    root_path = Path(root_dir)
    
    for file_path in root_path.rglob("*.py"):
        # Skip __pycache__ directories
        if "__pycache__" in str(file_path):
            continue
        
        # Skip if it's actually a directory (though .py shouldn't be)
        if file_path.is_file():
            python_files.append(file_path)
    
    # Sort files for consistent output
    python_files.sort(key=lambda x: str(x))
    return python_files

def combine_files_to_single(output_file="all_code.py", root_dir="."):
    """Combine all Python files into a single file with headers."""
    python_files = collect_python_files(root_dir)
    
    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write("# ============================================================================\n")
        outfile.write("# COMBINED PROJECT CODE\n")
        outfile.write(f"# Total files: {len(python_files)}\n")
        outfile.write("# ============================================================================\n\n")
        
        for i, file_path in enumerate(python_files, 1):
            # Write header
            outfile.write(f"\n{'=' * 80}\n")
            outfile.write(f"# FILE {i}/{len(python_files)}: {file_path}\n")
            outfile.write(f"{'=' * 80}\n\n")
            
            try:
                # Read and write file content
                with open(file_path, "r", encoding="utf-8") as infile:
                    content = infile.read()
                    outfile.write(content)
                    
                    # Add newline if file doesn't end with one
                    if content and not content.endswith("\n"):
                        outfile.write("\n")
                        
            except Exception as e:
                outfile.write(f"# ERROR reading file: {e}\n\n")
        
        # Write summary
        outfile.write(f"\n{'=' * 80}\n")
        outfile.write("# SUMMARY\n")
        outfile.write(f"# Files combined: {len(python_files)}\n")
        outfile.write("# File list:\n")
        for file_path in python_files:
            outfile.write(f"#   {file_path}\n")
        outfile.write(f"{'=' * 80}\n")
    
    print(f"✓ Combined {len(python_files)} files into '{output_file}'")
    return python_files

def main():
    # If a directory is provided as argument, use it
    root_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    output_file = "all_project_code.py"
    
    print(f"Scanning for Python files in: {os.path.abspath(root_dir)}")
    
    try:
        files = combine_files_to_single(output_file, root_dir)
        
        print("\nFiles included:")
        for file_path in files:
            print(f"  {file_path}")
            
        # Print file size
        output_size = os.path.getsize(output_file)
        print(f"\nOutput file size: {output_size:,} bytes ({output_size/1024:.1f} KB)")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()