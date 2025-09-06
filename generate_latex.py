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
    Generate the complete LaTeX document content.
    
    Args:
        parts (list): List of tuples (part_name, chapters)
        
    Returns:
        str: Complete LaTeX document content
    """
    latex_content = []
    
    # Document header
    latex_content.extend([
        r"\documentclass[openany,10pt,UTF8]{ctexbook}",
        r"\usepackage[a4paper,twoside,width=15cm]{geometry}",
        "",
        r"\title{Tech Management}",
        r"\author{Han Rui}",
        r"\date{\today}",
        "",
        r"\begin{document}",
        "",
        r"\maketitle",
        r"\tableofcontents",
        ""
    ])
    
    # Generate parts and chapters
    for part_name, chapters in parts:
        latex_content.append(f"\\part{{{part_name}}}")
        
        for chapter_name in chapters:
            latex_content.append(f"\\chapter{{{chapter_name}}}")
            latex_content.append(f"\\input{{ideas/{part_name}/{chapter_name}}}")
        
        latex_content.append("")  # Empty line after each part
    
    # Document footer
    latex_content.extend([
        r"\end{document}"
    ])
    
    return "\n".join(latex_content)

def main():
    """
    Main function to generate LaTeX structure.
    """
    # Default paths
    ideas_path = "src/ideas"
    output_file = sys.argv[1] if len(sys.argv) > 1 else None
    
    try:
        # Scan the ideas directory
        parts = scan_ideas_directory(ideas_path)
        
        if not parts:
            print("Warning: No parts with chapters found in ideas directory", file=sys.stderr)
            return 1
        
        # Generate LaTeX content
        latex_content = generate_latex_content(parts)
        
        # Output to file or stdout
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            print(f"LaTeX structure generated: {output_file}")
        else:
            print(latex_content)
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())