#!/usr/bin/env python3
"""
LaTeX Structure Auto-Generator

This script automatically generates the LaTeX document structure by scanning
the ideas directory and creating \\part and \\chapter entries based on the
directory hierarchy.

Usage:
    python3 generate_latex.py [output_file]
    
The script will:
1. Scan the src/ideas/ directory for subdirectories (parts)
2. For each part directory, scan for .tex files (chapters)
3. Generate a complete LaTeX document with proper structure
4. Output to specified file or stdout
"""

import os
import sys
from pathlib import Path

def scan_ideas_directory(ideas_path):
    """
    Scan the ideas directory and return structured data for LaTeX generation.
    
    Args:
        ideas_path (str): Path to the ideas directory
        
    Returns:
        list: List of tuples (part_name, chapters) where chapters is a list of chapter names
    """
    ideas_dir = Path(ideas_path)
    if not ideas_dir.exists():
        raise FileNotFoundError(f"Ideas directory not found: {ideas_path}")
    
    parts = []
    
    # Get all subdirectories (parts) and sort them
    part_dirs = [d for d in ideas_dir.iterdir() if d.is_dir()]
    part_dirs.sort(key=lambda x: x.name)
    
    for part_dir in part_dirs:
        part_name = part_dir.name
        chapters = []
        
        # Get all .tex files in this part directory
        tex_files = [f for f in part_dir.iterdir() if f.is_file() and f.suffix == '.tex']
        tex_files.sort(key=lambda x: x.name)
        
        for tex_file in tex_files:
            chapter_name = tex_file.stem  # filename without extension
            chapters.append(chapter_name)
        
        if chapters:  # Only add parts that have chapters
            parts.append((part_name, chapters))
    
    return parts

def generate_latex_content(parts):
    """
    Generate LaTeX content with parts and chapters based on the directory structure.
    This function only generates the content section, preserving the existing
    document structure in tech-management.tex.
    
    Args:
        parts (list): List of tuples (part_name, chapters)
        
    Returns:
        str: LaTeX content for parts and chapters only
    """
    latex_content = []
    
    # Generate parts and chapters only (no document header/footer)
    for part_name, chapters in parts:
        latex_content.append(f"\\part{{{part_name}}}")
        
        for chapter_name in chapters:
            latex_content.append(f"\\chapter{{{chapter_name}}}")
            latex_content.append(f"\\input{{ideas/{part_name}/{chapter_name}}}")
        
        latex_content.append("")  # Empty line after each part
    
    return "\n".join(latex_content)

def main():
    """
    Main function that scans the ideas directory and updates the existing
    tech-management.tex file with new structure while preserving the document setup.
    
    Args:
        output_file (str): Path to the LaTeX file to update
        
    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    if len(sys.argv) != 2:
        print("Usage: python3 generate_latex.py <tex_file.tex>")
        print("")
        print("This script scans the src/ideas directory and updates")
        print("the LaTeX file with automatic part and chapter structure.")
        return 1
    
    tex_file = sys.argv[1]
    
    try:
        # Get the directory containing this script
        script_dir = Path(__file__).parent
        ideas_path = script_dir / "src" / "ideas"
        
        if not ideas_path.exists():
            print(f"Error: Ideas directory not found at {ideas_path}")
            return 1
        
        # Read existing tex file
        tex_path = Path(tex_file)
        if not tex_path.exists():
            print(f"Error: LaTeX file not found at {tex_file}")
            return 1
            
        with open(tex_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Scan the ideas directory
        parts = scan_ideas_directory(ideas_path)
        
        if not parts:
            print("Warning: No content found in ideas directory")
            return 1
        
        # Generate new content section
        new_content_section = generate_latex_content(parts)
        
        # Find the content section boundaries
        import re
        # Match everything from \tableofcontents to \end{document}
        pattern = r'(.*?\\tableofcontents\s*\n)(.*?)(\\end\{document\}.*?)'
        match = re.search(pattern, original_content, re.DOTALL)
        
        if not match:
            print("Error: Could not find content section in LaTeX file")
            return 1
        
        # Reconstruct the file with new content
        header = match.group(1)
        footer = match.group(3)
        updated_content = header + "\n" + new_content_section + "\n\n" + footer
        
        # Write updated content back to file
        with open(tex_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"LaTeX structure updated in {tex_file}")
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())