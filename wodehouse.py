import requests
from toolz.curried import first, map, pipe, pluck


next_page_url = 'https://gutendex.com/books?search=wodehouse'
results = []

while next_page_url:
    response = requests.get(next_page_url)
    response_content = response.json()

    results.extend(response_content['results'])
    next_page_url = response_content.get('next')

wodehouse_books = [
    book
    for book in results
    if "Wodehouse" in book['authors'][0]['name']
]

download_urls = pipe(
    wodehouse_books,
    pluck('formats'),
    map(
        lambda book_format: (
            download_url
            for mime_type, download_url in book_format.items()
            if mime_type.startswith('text/plain')
        )
    ),
    # take one, as sometimes there's more than one plain text format per book, e.g. UTF-8 and ASCII
    map(first),
    # flatten
    list
)

print(download_urls)
print(f"found {len(download_urls)} books")
