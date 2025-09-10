#!/usr/bin/env python3
"""
print_chord.py

Fetches a Guitarians chord print page and saves it as a PDF using Playwright and ReportLab.
Usage: uv run print_chord.py <folder_name> <clicks>
"""
import sys
import argparse
from pathlib import Path
from urllib.parse import unquote
import re
from playwright.sync_api import sync_playwright
from pathlib import Path
from PyPDF2 import PdfMerger

def parse_chord_url(url):
    """Extract artist folder name and song name from Guitarians chord print URL."""
    # Extract the ID number
    pattern = r"/chord/print/(\d+)/"
    match = re.search(pattern, url)
    if not match:
        raise ValueError(f"Invalid chord print URL format: {url}")
    
    # Decode the URL-encoded path
    song_id = unquote(match.group(1))    
    return song_id


def print_chord(url, output_path, clicks):
    """Fetch chord page and save as PDF at the specified path using Playwright's PDF generation."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_selector('body')
        page.wait_for_selector('li.twoinoneBtn')
        page.click('li.twoinoneBtn')
        page.wait_for_selector('li.fontLargerBtn')
        # page.click('li.fontSmallerBtn')
        for _ in range(clicks):
            page.click('li.fontLargerBtn')
        page.pdf(path=str(output_path))
        browser.close()


def preprocess_url(raw_url):
    """Ensure URL has /print/ segment and append default targetCapo parameter."""
    # Strip any existing query parameters
    base = raw_url
    # Insert 'print/' after '/chord/' if missing
    if '/chord/print/' not in base:
        base = base.replace('/chord/', '/chord/print/', 1)
    # Append default capo parameter
    return base 


def process_urls_from_file(url_file, folder_name, clicks):
    """Process each URL from the given file."""
    with open(url_file, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]

    for url in urls:
        # Preprocess raw URL to ensure correct print path and query
        processed_url = preprocess_url(url)
        try:
            # Parse URL to get artist and song names
            song_name = parse_chord_url(processed_url)

            # Create output directory structure
            chord_dir = Path("chord")
            artist_dir = chord_dir / folder_name
            artist_dir.mkdir(parents=True, exist_ok=True)

            # Set output path
            output_path = artist_dir / f"{song_name}.pdf"

            # Generate PDF
            print_chord(processed_url, output_path, clicks)
            print(f"Saved PDF to {output_path}")
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")


def merge_pdfs(folder_name):
    """Merge all PDFs in chord/{folder_name} into a single PDF."""
    chord_dir = Path("chord") / folder_name
    pdf_files = sorted(chord_dir.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in {chord_dir}")
        return
    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(str(pdf))
    output_file = chord_dir / f"{folder_name}.pdf"
    merger.write(str(output_file))
    merger.close()
    print(f"Merged {len(pdf_files)} PDFs into {output_file}")
    # Remove individual PDF files after merge
    for pdf in pdf_files:
        try:
            pdf.unlink()
        except Exception as e:
            print(f"Failed to delete {pdf}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Guitarians chord print pages and save as PDFs")
    parser.add_argument("folder_name", help="Name of the folder to save PDFs in (e.g., 'batch 1')")
    parser.add_argument("clicks", type=int, help="Number of times to click the font larger button")

    args = parser.parse_args()
    folder_name = args.folder_name
    clicks = args.clicks

    url_file = "url.txt"
    if not Path(url_file).exists():
        print(f"Error: {url_file} not found")
        sys.exit(1)

    process_urls_from_file(url_file, folder_name, clicks)
    merge_pdfs(folder_name)