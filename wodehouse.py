from toolz.curried import pipe, pluck, map, first
import json
from requests import request

response = request('get', 'https://gutendex.com/books?search=wodehouse')

# TODO this is only the first page! we need all the Wodehouse.
books = json.loads(response.content)

downloadUrls = pipe(
    books['results'],
    pluck('formats'),
    map(lambda format: (downloadUrl for mimeType, downloadUrl in format.items() if mimeType.startswith('text/plain'))),
    # take one, as sometimes there's more than one plain text format per book, e.g. UTF-8 and ASCII
    map(first),
    # flatten
    list
)

print(downloadUrls)
