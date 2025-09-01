#!/usr/bin/env python3
"""
Script to merge all PDF files from chord batch folders into one PDF.
The PDFs are ordered by batch number in ascending order.
"""

import os
import re
from pathlib import Path
from PyPDF2 import PdfWriter, PdfReader


def extract_batch_number(batch_folder_name):
    """Extract the batch number from folder name like 'batch_4' -> 4"""
    match = re.search(r'batch_(\d+)', batch_folder_name)
    return int(match.group(1)) if match else 0


def get_batch_folders(chord_dir):
    """Get all batch folders sorted by batch number"""
    batch_folders = []
    
    for item in os.listdir(chord_dir):
        item_path = os.path.join(chord_dir, item)
        if os.path.isdir(item_path) and item.startswith('batch_'):
            batch_folders.append(item)
    
    # Sort by batch number
    batch_folders.sort(key=extract_batch_number)
    return batch_folders


def get_pdf_files(folder_path):
    """Get all PDF files from a folder, sorted alphabetically"""
    pdf_files = []
    
    if os.path.exists(folder_path):
        for file in os.listdir(folder_path):
            if file.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(folder_path, file))
    
    return sorted(pdf_files)


def merge_pdfs():
    """Main function to merge all PDF files"""
    # Define paths
    chord_dir = Path('chord')
    output_file = 'merged_chord_sheets.pdf'
    
    if not chord_dir.exists():
        print(f"Error: Chord directory '{chord_dir}' not found!")
        return
    
    # Get all batch folders in order
    batch_folders = get_batch_folders(chord_dir)
    
    if not batch_folders:
        print("No batch folders found in chord directory!")
        return
    
    print(f"Found {len(batch_folders)} batch folders:")
    for folder in batch_folders:
        print(f"  - {folder}")
    
    # Create PDF writer
    pdf_writer = PdfWriter()
    total_pages = 0
    processed_files = []
    
    # Process each batch folder in order
    for batch_folder in batch_folders:
        batch_path = chord_dir / batch_folder
        pdf_files = get_pdf_files(batch_path)
        
        if pdf_files:
            print(f"\nProcessing {batch_folder} ({len(pdf_files)} PDF files):")
            
            for pdf_file in pdf_files:
                try:
                    # Read the PDF file
                    pdf_reader = PdfReader(pdf_file)
                    pages_in_file = len(pdf_reader.pages)
                    
                    # Add all pages to the writer
                    for page in pdf_reader.pages:
                        pdf_writer.add_page(page)
                    
                    total_pages += pages_in_file
                    processed_files.append(os.path.basename(pdf_file))
                    print(f"  ✓ {os.path.basename(pdf_file)} ({pages_in_file} pages)")
                    
                except Exception as e:
                    print(f"  ✗ Error processing {os.path.basename(pdf_file)}: {e}")
        else:
            print(f"\nSkipping {batch_folder} (no PDF files found)")
    
    # Write the merged PDF
    if total_pages > 0:
        try:
            with open(output_file, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)
            
            print(f"\n🎉 Successfully merged {len(processed_files)} PDF files!")
            print(f"📄 Total pages: {total_pages}")
            print(f"💾 Output file: {output_file}")
            
            # Show summary of processed files
            print(f"\nProcessed files in order:")
            for i, filename in enumerate(processed_files, 1):
                print(f"  {i:2d}. {filename}")
                
        except Exception as e:
            print(f"\n❌ Error writing merged PDF: {e}")
    else:
        print("\n⚠️  No PDF files were processed!")


if __name__ == "__main__":
    merge_pdfs() 