# Guitarians Tools

## Scripts

### 1. url_to_pdf.py
Convert Guitarians chord URLs to PDF files.

```bash
uv run url_to_pdf.py -i <input_file> -o <output_file> [-clicks <number>]
```

**Parameters:**
- `-i, --input`: Input text file containing the chord URL (required)
- `-o, --output`: Output PDF file path (required)
- `-clicks, --clicks`: Number of times to click the font larger button (default: 0)

**Example:**
```bash
uv run url_to_pdf.py -i songs/eason.txt -o eason_chord.pdf -clicks 3
```

### 2. list_artist_songs.py
Scrape song lists from Guitarians artist profile pages.

```bash
uv run list_artist_songs.py
```

**Note:** Currently configured to scrape 張敬軒 (Hins Cheung) artist page. Edit the URL in the script to change the target artist.

### 3. unicode_fix.py
Fix URL-encoded Unicode characters in text files to display properly.

```bash
uv run unicode_fix.py -o <file_path>
```

**Parameters:**
- `-o, --output`: Path to the text file to fix Unicode characters in (required)

**Example:**
```bash
uv run unicode_fix.py -o songs/size1.txt
```

### 4. merge_pdfs.py
Merge multiple PDF files into a single PDF.

```bash
uv run pdfs/merge_pdfs.py -o <output_file> [-i <input_file> | -dir <directory> | <pdf_files>...]
```

**Parameters:**
- `-o, --output`: Output PDF file path (required)
- `-i, --input`: Text file containing list of PDF files to merge (one per line)
- `-dir, --directory`: Directory containing PDF files to merge
- `<pdf_files>`: PDF files to merge directly (alternative to -i or -dir)

**Examples:**
```bash
# Merge PDFs from a text file list
uv run merge_pdfs.py -o merged.pdf -i pdf_list.txt

# Merge all PDFs in a directory
uv run merge_pdfs.py -o combined.pdf -dir ./chord/

# Merge specific PDF files directly
uv run merge_pdfs.py -o final.pdf file1.pdf file2.pdf file3.pdf
```
