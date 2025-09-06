#!/usr/bin/env python3
"""
LaTeX Input Expander

This script recursively expands all \input{} commands in a LaTeX document,
creating a single consolidated file that contains all the content from
included files. This is necessary because pandoc cannot handle LaTeX \input{}
commands when converting to HTML.

The script:
1. Reads the main LaTeX file
2. Finds all \input{filename} commands
3. Recursively reads and includes the content of referenced files
4. Outputs a single expanded LaTeX file with all content inline

Usage:
    python3 expand_latex.py input_file.tex output_file.tex

Example:
    python3 expand_latex.py src/tech-management.tex build/expanded.tex
"""

import os
import re
import sys

def expand_input(content, base_dir):
    """
    Recursively expand \\input{} commands in LaTeX content.
    
    This function searches for LaTeX \input{filename} commands and replaces
    them with the actual content of the referenced files. It handles:
    - Relative paths from the base directory
    - Automatic .tex extension addition if not specified
    - Recursive expansion of nested \input commands
    - Error handling for missing files
    
    Args:
        content (str): The LaTeX content to process
        base_dir (str): Base directory for resolving relative file paths
        
    Returns:
        str: LaTeX content with all \input{} commands expanded
    """
    def replace_input(match):
        """
        Replace a single \input{} command with the content of the referenced file.
        
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
    Main function that handles command line arguments and file processing.
    
    Reads the input LaTeX file, expands all \input{} commands recursively,
    and writes the result to the output file. Creates output directory if needed.
    """
    # Check command line arguments
    if len(sys.argv) != 3:
        print("Usage: python3 expand_latex.py input_file.tex output_file.tex")
        print("")
        print("This script expands all \\input{} commands in a LaTeX file,")
        print("creating a single consolidated file for pandoc conversion.")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Get the directory of the input file for resolving relative paths
    base_dir = os.path.dirname(input_file)
    
    try:
        # Read the main LaTeX file
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
        
    except FileNotFoundError:
        print(f"Error: Input file {input_file} not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()