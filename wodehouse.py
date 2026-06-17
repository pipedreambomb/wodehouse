import requests

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
