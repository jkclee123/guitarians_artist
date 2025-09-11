#!/usr/bin/env python3
"""
print_chord.py

Fetches a Guitarians chord print page and saves it as a PDF using Playwright.
Usage: uv run print_chord.py -i <input_file> -o <output_file> [-clicks <number>]
"""
import argparse
from pathlib import Path
from urllib.parse import unquote
import re
from playwright.sync_api import sync_playwright

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


def process_url_from_file(input_file, output_path, clicks):
    """Process the URL from the given file and save as PDF."""
    with open(input_file, 'r', encoding='utf-8') as f:
        url = f.read().strip()

    if not url:
        raise ValueError(f"No URL found in {input_file}")

    # Preprocess raw URL to ensure correct print path and query
    processed_url = preprocess_url(url)

    # Generate PDF
    print_chord(processed_url, output_path, clicks)
    print(f"Saved PDF to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Guitarians chord print page and save as PDF")
    parser.add_argument("-i", "--input", required=True, help="Input text file containing the chord URL")
    parser.add_argument("-o", "--output", required=True, help="Output PDF file path")
    parser.add_argument("-clicks", "--clicks", type=int, default=0, help="Number of times to click the font larger button (default: 0)")

    args = parser.parse_args()
    input_file = args.input
    output_path = Path(args.output)
    clicks = args.clicks

    process_url_from_file(input_file, output_path, clicks)