import os
import re
import requests
import time

next_page_url = 'https://gutendex.com/books?search=wodehouse'
results = []

while next_page_url:
    response = requests.get(next_page_url)
    response_content = response.json()

    results.extend(response_content['results'])
    next_page_url = response_content.get('next')

download_urls = {
    book['title']: download_url
    for book in results
    if any("Wodehouse, P. G. (Pelham Grenville)" == author['name'] 
        for author in book['authors'])
    for mime_type, download_url in book['formats'].items()
    if mime_type.startswith('text/plain')
}

print(download_urls)
print(f"found {len(download_urls)} books")

os.makedirs("output", exist_ok=True)

for title, url in download_urls.items():
    # Sanitize the title so it's a valid filename
    safe_title = re.sub(r'[\\/*?:"<>|]', "", title)
    filepath = os.path.join("output", f"{safe_title}.txt")
    
    if os.path.exists(filepath):
        print(f"Skipping '{safe_title}' (already downloaded)")
        continue
        
    print(f"Downloading '{safe_title}'...")
    try:
        # Be polite to the Gutenberg servers
        time.sleep(1)
        
        book_response = requests.get(url)
        book_response.raise_for_status()
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(book_response.text)
            
    except Exception as e:
        print(f"Failed to download '{safe_title}': {e}")

print("All books downloaded!")
