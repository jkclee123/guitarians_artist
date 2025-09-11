#!/usr/bin/env python3
"""
unicode_fix.py

Rewrites a text file with URL-encoded Unicode characters to display them correctly.
Usage: uv run unicode_fix.py -i <file_path>
"""
import argparse
from pathlib import Path
from urllib.parse import unquote
import sys


def fix_unicode_in_file(file_path):
    """Fix Unicode characters in the specified file."""
    try:
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # URL-decode the content to display Unicode characters properly
        fixed_content = unquote(content)

        # Write the fixed content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)

        print(f"Successfully fixed Unicode characters in {file_path}")
        print("Preview of fixed content:")
        print("-" * 50)
        print(fixed_content[:500] + "..." if len(fixed_content) > 500 else fixed_content)
        print("-" * 50)

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Fix URL-encoded Unicode characters in text files to display properly"
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Path to the text file to fix Unicode characters in"
    )

    args = parser.parse_args()
    file_path = Path(args.input)

    if not file_path.exists():
        print(f"Error: File '{file_path}' does not exist")
        sys.exit(1)

    fix_unicode_in_file(file_path)


if __name__ == "__main__":
    main()
