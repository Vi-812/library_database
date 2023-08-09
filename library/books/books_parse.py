import requests
import json
from loguru import logger
from .models import Category, Author, Book
from django.core.files.base import ContentFile
from tempfile import NamedTemporaryFile
import os


log_file_path = '../logfile.log'
logger.add(log_file_path, format='{time} {level} {message}', level='INFO')


def parser(url):
    adding_books_text = requests.get(url).text
    adding_books = json.loads(adding_books_text)

    added_count = 0
    duplicate_count = 0
    error_count = 0

    for book in adding_books:
        title = book.get("title")
        isbn = book.get("isbn")

        if Book.objects.filter(title=title, isbn=isbn).exists():
            duplicate_count += 1
            continue

        page_count = book.get("pageCount")
        published_date = book.get("publishedDate")
        if published_date:
            published_date = published_date.get("$date")
        else:
            logger.warning(f"Книга {title} ({isbn}) не имеет даты публикации!")
        thumbnail_url = book.get("thumbnailUrl")
        short_description = book.get("shortDescription")
        long_description = book.get("longDescription")
        status = book.get("status")
        authors = book.get("authors")
        categories = book.get("categories")

        author_objs = []
        for author_name in authors:
            author_obj, _ = Author.objects.get_or_create(name=author_name)
            author_objs.append(author_obj)

        book_obj = Book(
            title=title,
            isbn=isbn,
            page_count=page_count,
            published_date=published_date,
            thumbnail_url=thumbnail_url,
            short_description=short_description,
            long_description=long_description,
            status=status
        )
        book_obj.save()

        for author_obj in author_objs:
            book_obj.authors.add(author_obj)

        if thumbnail_url:
            temp_image = NamedTemporaryFile(delete=True)
            temp_image.write(requests.get(thumbnail_url).content)
            temp_image.flush()

            image_name = os.path.basename(thumbnail_url)
            content_file = ContentFile(temp_image.read(), name=image_name)

            book_obj.cover_image.save(image_name, content_file)

        book_obj.save()

        added_count += 1

    return {
        "Added": added_count,
        "Duplicates": duplicate_count,
        "Errors": error_count
    }
