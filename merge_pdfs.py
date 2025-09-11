#!/usr/bin/env python3
"""
General-purpose PDF merger script.

Usage:
    uv run chord/merge_pdfs.py -o output.pdf -i pdf_list.txt
    uv run chord/merge_pdfs.py -o merged.pdf -dir /path/to/pdfs
    uv run chord/merge_pdfs.py -o combined.pdf input1.pdf input2.pdf input3.pdf
"""

import sys
import os
import argparse
from pathlib import Path
from PyPDF2 import PdfWriter, PdfReader


def merge_pdfs_from_list(pdf_files, output_path):
    """
    Merge multiple PDF files into one.

    Args:
        pdf_files (list): List of PDF file paths to merge
        output_path (str): Path for the output merged PDF file

    Returns:
        tuple: (success: bool, total_pages: int, processed_files: list)
    """
    if not pdf_files:
        print("Error: No PDF files provided!")
        return False, 0, []

    # Create PDF writer
    pdf_writer = PdfWriter()
    total_pages = 0
    processed_files = []
    failed_files = []

    print(f"Merging {len(pdf_files)} PDF files...")

    for i, pdf_file in enumerate(pdf_files, 1):
        pdf_path = Path(pdf_file)

        # Check if file exists
        if not pdf_path.exists():
            print(f"  {i:2d}. ✗ File not found: {pdf_file}")
            failed_files.append(pdf_file)
            continue

        # Check if it's actually a PDF
        if pdf_path.suffix.lower() != '.pdf':
            print(f"  {i:2d}. ✗ Not a PDF file: {pdf_file}")
            failed_files.append(pdf_file)
            continue

        try:
            # Read the PDF file
            with open(pdf_path, 'rb') as file:
                pdf_reader = PdfReader(file)
                pages_in_file = len(pdf_reader.pages)

                # Add all pages to the writer
                for page in pdf_reader.pages:
                    pdf_writer.add_page(page)

                total_pages += pages_in_file
                processed_files.append(pdf_path.name)
                print(f"  {i:2d}. ✓ {pdf_path.name} ({pages_in_file} pages)")

        except Exception as e:
            print(f"  {i:2d}. ✗ Error processing {pdf_path.name}: {e}")
            failed_files.append(pdf_file)

    # Write the merged PDF if we have any pages
    if total_pages > 0:
        try:
            with open(output_path, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)

            print(f"\n🎉 Successfully merged {len(processed_files)} PDF files!")
            print(f"📄 Total pages: {total_pages}")
            print(f"💾 Output file: {output_path}")

            if failed_files:
                print(f"\n⚠️  {len(failed_files)} files failed to process:")
                for failed_file in failed_files:
                    print(f"  - {failed_file}")

            return True, total_pages, processed_files

        except Exception as e:
            print(f"\n❌ Error writing merged PDF: {e}")
            return False, 0, []
    else:
        print("\n⚠️  No PDF files were successfully processed!")
        return False, 0, []


def read_pdf_list_from_file(file_path):
    """Read a list of PDF files from a text file (one filename per line)."""
    pdf_files = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):  # Skip empty lines and comments
                    pdf_files.append(line)
    except Exception as e:
        print(f"Error reading file list: {e}")
        return []

    return pdf_files


def find_pdfs_in_directory(directory):
    """Find all PDF files in a directory (non-recursive)."""
    pdf_files = []
    dir_path = Path(directory)

    if not dir_path.exists() or not dir_path.is_dir():
        print(f"Error: Directory not found: {directory}")
        return []

    for file_path in dir_path.iterdir():
        if file_path.is_file() and file_path.suffix.lower() == '.pdf':
            pdf_files.append(str(file_path))

    # Sort alphabetically
    pdf_files.sort()
    return pdf_files


def main():
    parser = argparse.ArgumentParser(
        description="Merge multiple PDF files into one",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -o output.pdf -i pdf_list.txt
  %(prog)s -o merged.pdf -dir ./chord/
  %(prog)s -o combined.pdf file1.pdf file2.pdf file3.pdf
        """
    )

    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output PDF file path'
    )

    parser.add_argument(
        '-i', '--input',
        help='Text file containing list of PDF files (one per line)'
    )

    parser.add_argument(
        '-dir', '--directory',
        help='Directory containing PDF files to merge'
    )

    parser.add_argument(
        'pdf_files',
        nargs='*',
        help='PDF files to merge directly (alternative to -i or -dir)'
    )

    args = parser.parse_args()

    # Determine the list of PDF files to process
    pdf_files = []

    if args.input:
        # Read from file
        pdf_files = read_pdf_list_from_file(args.input)
    elif args.directory:
        # Find PDFs in directory
        pdf_files = find_pdfs_in_directory(args.directory)
    else:
        # Use command line arguments
        pdf_files = args.pdf_files

    if not pdf_files:
        parser.print_help()
        sys.exit(1)

    # Merge the PDFs
    success, total_pages, processed_files = merge_pdfs_from_list(pdf_files, args.output)

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
