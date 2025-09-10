# 🎸 Guitarians Artist Chord Scraper

A Python tool for scraping and organizing guitar chord sheets from [Guitarians.com](https://zh-hk.guitarians.com), a popular Cantopop guitar chord resource.

## 📋 Overview

This project provides automated tools to:
- Scrape song lists from artist profile pages
- Download guitar chord sheets as PDF files
- Merge multiple chord sheets into organized collections
- Organize data by artists and batches

## 🚀 Features

- **Artist Song Scraper**: Extract complete song lists from artist profiles
- **PDF Chord Downloader**: Convert chord sheets to high-quality PDFs with customizable formatting
- **Batch PDF Merger**: Combine multiple chord sheets into single organized documents
- **Automated Organization**: Smart folder structure for artists and chord collections

## 📦 Dependencies

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager
- Playwright for browser automation
- BeautifulSoup4 for HTML parsing
- PyPDF2 for PDF manipulation

## 🛠️ Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd guitarians-artist
```

2. Install dependencies using uv:
```bash
uv sync
```

3. Install Playwright browsers:
```bash
uv run playwright install
```

## 📖 Usage

### 1. Scrape Artist Song List

Run the artist scraper to get all songs from a specific artist:

```bash
uv run artist.py
```

This will:
- Scrape the configured artist page (currently set to 張敬軒/Hins Cheung)
- Extract all song names
- Save them to `artist/{artist_name}.txt`

### 2. Download Chord Sheets

Prepare a `url.txt` file with chord sheet URLs, then run:

```bash
uv run print_chord.py "batch 1" 5
```

This command uses:
- `"batch 1"` as the folder name for organizing PDFs
- `5` as the number of font size increases

This will:
- Download each chord sheet as a PDF
- Apply formatting optimizations (larger font, two-in-one layout)
- Save PDFs to `chord/{folder_name}/`
- Merge all PDFs into a single file

### 3. Merge Existing Chord PDFs

To merge chord sheets from batch folders:

```bash
uv run merge_chord_pdfs.py
```

This will:
- Find all `batch_*` folders in the `chord/` directory
- Process PDFs in numerical order
- Create a merged `merged_chord_sheets.pdf`

## 📁 Project Structure

```
guitarians-artist/
├── artist/                 # Artist song lists (scraped data)
├── songs/                  # Individual song URLs
├── chord/                  # Generated PDF chord sheets
├── artist.py              # Artist profile scraper
├── print_chord.py         # PDF chord downloader
├── merge_chord_pdfs.py    # PDF merger utility
├── url.txt                # Input URLs for downloading
└── pyproject.toml         # Project configuration
```

## 🔧 Configuration

### Artist Scraper (`artist.py`)
- Edit the `url` variable to change the target artist
- Supports any Guitarians.com artist profile URL

### Chord Downloader (`print_chord.py`)
- Modify `folder_name` variable to organize outputs
- Add chord URLs to `url.txt` (one per line)
- Customize PDF formatting in the `print_chord()` function

## 🎵 Supported Artists

The project includes data for popular Cantopop artists including:
- 張敬軒 (Hins Cheung)
- 陳奕迅 (Eason Chan)
- And many more in the `songs/` directory

## 📄 Output Formats

- **Artist Lists**: Plain text files with song names
- **Chord Sheets**: High-quality PDFs optimized for printing
- **Merged Collections**: Single PDF files combining multiple songs
