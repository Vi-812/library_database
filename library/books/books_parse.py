import requests
import json
from .models import Category, Author, Book


def parser(url):
    adding_books_text = requests.get(url).text
    adding_books = json.loads(adding_books_text)
    for book in adding_books:
        title = book.get("title")
        isbn = book.get("isbn")
        page_count = book.get("pageCount")
        published_date = book.get("publishedDate")
        if published_date:
            published_date = published_date.get("$date")
        else:
            print(f"ERROR {isbn}")
        thumbnail_url = book.get("thumbnailUrl")
        short_description = book.get("shortDescription")
        long_description = book.get("longDescription")
        status = book.get("status")
        authors = book.get("authors")
        categories = book.get("categories")


        if len(categories) > 2:
            print(categories, isbn)
