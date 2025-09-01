from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import unquote
import re

def scrape_song_names():
    # URL of the target webpage
    url = "https://zh-hk.guitarians.com/artist/45-%E5%BC%B5%E6%95%AC%E8%BB%92"
    m = re.search(r"/artist/\d+-(.+)$", url)
    if not m:
        raise ValueError(f"Could not extract artist name from URL: {url}")
    artist_name = unquote(m.group(1))
    file_name = artist_name.replace(" ", "_")
    
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Set viewport size
        page.set_viewport_size({"width": 1280, "height": 800})
        
        # Navigate to the page
        page.goto(url)
        
        # Wait for the content to load
        page.wait_for_selector('.score-name')
        
        # Get the page content
        content = page.content()
        
        # Close the browser
        browser.close()
    
    # Create BeautifulSoup object to parse HTML
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find all score-name elements that are not under sub-score-list
    song_names = set()
    score_names = soup.find_all(class_="score-name")
    
    for score_name in score_names:
        if not score_name.find_parent(class_="sub-score-list"):
            # Remove any nested label tags before extracting text
            for label in score_name.find_all('label'):
                label.decompose()
            song_name = score_name.get_text(strip=True)
            song_names.add(song_name)
    
    # Write song names to file
    artist_dir = Path("artist")
    artist_dir.mkdir(exist_ok=True)  # Create artist directory if it doesn't exist
    output_file = artist_dir / f"{file_name}.txt"
    output_file.write_text(f"{artist_name}\n" + ", ".join(sorted(song_names)), encoding='utf-8')
    print(f"\nSuccessfully wrote {len(song_names)} song names to {output_file}")

if __name__ == "__main__":
    scrape_song_names()
