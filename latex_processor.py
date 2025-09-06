#!/usr/bin/env python3
"""
LaTeX Document Processor

This script combines the functionality of generate_latex.py and expand_latex.py:
1. Automatically generates LaTeX structure from ideas directory
2. Expands all \\input{} commands for pandoc compatibility

Usage:
    python3 latex_processor.py <input_tex_file> <output_expanded_file>
    
Example:
    python3 latex_processor.py src/tech-management.tex build/expanded.tex
"""

import os
import re
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

def update_latex_structure(tex_file, ideas_path):
    """
    Update the LaTeX file structure based on ideas directory content.
    
    Args:
        tex_file (str): Path to the LaTeX file to update
        ideas_path (str): Path to the ideas directory
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Read existing tex file
        tex_path = Path(tex_file)
        if not tex_path.exists():
            print(f"Error: LaTeX file not found at {tex_file}")
            return False
            
        with open(tex_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Scan the ideas directory
        parts = scan_ideas_directory(ideas_path)
        
        if not parts:
            print("Warning: No content found in ideas directory")
            return False
        
        # Generate new content section
        new_content_section = generate_latex_content(parts)
        
        # Find the content section boundaries
        # Match everything from \tableofcontents to \end{document}
        pattern = r'(.*?\\tableofcontents\s*\n)(.*?)(\\end\{document\}.*?)'
        match = re.search(pattern, original_content, re.DOTALL)
        
        if not match:
            print("Error: Could not find content section in LaTeX file")
            return False
        
        # Reconstruct the file with new content
        header = match.group(1)
        footer = match.group(3)
        updated_content = header + "\n" + new_content_section + "\n\n" + footer
        
        # Write updated content back to file
        with open(tex_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"LaTeX structure updated in {tex_file}")
        return True
        
    except Exception as e:
        print(f"Error updating LaTeX structure: {e}")
        return False

def expand_input(content, base_dir):
    """
    Recursively expand \\input{} commands in LaTeX content.
    
    This function searches for LaTeX \\input{filename} commands and replaces
    them with the actual content of the referenced files. It handles:
    - Relative paths from the base directory
    - Automatic .tex extension addition if not specified
    - Recursive expansion of nested \\input commands
    - Error handling for missing files
    
    Args:
        content (str): The LaTeX content to process
        base_dir (str): Base directory for resolving relative file paths
        
    Returns:
        str: LaTeX content with all \\input{} commands expanded
    """
    def replace_input(match):
        """
        Replace a single \\input{} command with the content of the referenced file.
        
        Args:
            match: Regular expression match object containing the filename
            
        Returns:
            str: Content of the referenced file, or error comment if file not found
        """
        input_file = match.group(1)
        
        # Add .tex extension if not present (LaTeX convention)
        if not input_file.endswith('.tex'):
            input_file += '.tex'
        
        # Resolve file path relative to base directory
        input_path = os.path.join(base_dir, input_file)
        
        if os.path.exists(input_path):
            with open(input_path, 'r', encoding='utf-8') as f:
                input_content = f.read()
            # Recursively expand any \input commands in the included file
            return expand_input(input_content, base_dir)
        else:
            print(f"Warning: File {input_path} not found")
            return f"% File not found: {input_file}"
    
    # Replace all \input{filename} with file contents using regex
    pattern = r'\\input\{([^}]+)\}'
    return re.sub(pattern, replace_input, content)

def main():
    """
    Main function that processes LaTeX files: updates structure and expands inputs.
    
    Args:
        input_file (str): Path to the input LaTeX file
        output_file (str): Path to the output expanded file
        
    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    if len(sys.argv) != 3:
        print("Usage: python3 latex_processor.py <input_tex_file> <output_expanded_file>")
        print("")
        print("This script:")
        print("1. Updates LaTeX structure based on ideas directory")
        print("2. Expands all \\\\input{} commands for pandoc compatibility")
        return 1
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        # Step 1: Update LaTeX structure
        script_dir = Path(__file__).parent
        ideas_path = script_dir / "src" / "ideas"
        
        if not update_latex_structure(input_file, ideas_path):
            return 1
        
        # Step 2: Expand input commands
        base_dir = os.path.dirname(input_file)
        
        # Read the updated LaTeX file
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Expand all \input commands recursively
        expanded_content = expand_input(content, base_dir)
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Write the expanded content to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(expanded_content)
        
        print(f"LaTeX file expanded and written to {output_file}")
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())