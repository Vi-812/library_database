import requests
import json
from loguru import logger
from .models import Category, Author, Book
from django.core.files.base import ContentFile
from tempfile import NamedTemporaryFile
import os
from dateutil.parser import parse

log_file_path = '../logfile.log'
logger.add(log_file_path, format='{time} {level} {message}', level='INFO')


def parse_categories(categories, parent=None):
    category_objs = []

    if not categories:
        new_products_category, _ = Category.objects.get_or_create(name="New products")
        category_objs.append(new_products_category)

    for category_name in categories:
        if category_name:
            category_obj, _ = Category.objects.get_or_create(name=category_name, parent=parent)
            category_objs.append(category_obj)

            if "children" in category_name:
                child_categories = category_name["children"]
                parse_categories(child_categories, parent=category_obj)

    return category_objs


def parser(url):
    try:
        adding_books_text = requests.get(url).text
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе данных: {e}")
        return {"Added": 0, "Duplicates": 0, "Errors": 0, "ReturnMessage": "Ошибка при запросе данных"}

    try:
        adding_books = json.loads(adding_books_text)
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка при декодировании JSON: {e}")
        return {"Added": 0, "Duplicates": 0, "Errors": 0, "ReturnMessage": "Ошибка при декодировании JSON"}

    added_count = 0
    duplicate_count = 0
    error_count = 0

    for book in adding_books:
        try:
            title = book.get("title")
            isbn = book.get("isbn")

            if Book.objects.filter(title=title, isbn=isbn).exists():
                duplicate_count += 1
                continue

            page_count = book.get("pageCount")
            published_date = book.get("publishedDate")
            if published_date:
                try:
                    published_date = published_date.get("$date")
                    published_date = parse(published_date).date().isoformat()
                except ValueError:
                    logger.warning(f"Книга {title} ({isbn}): неверный формат даты публикации!")
                    published_date = None
            else:
                logger.info(f"Книга {title} ({isbn}) не имеет даты публикации!")

            thumbnail_url = book.get("thumbnailUrl")
            short_description = book.get("shortDescription")
            long_description = book.get("longDescription")
            status = book.get("status")
            authors = book.get("authors")
            categories = book.get("categories", [])

            if not title \
                    or page_count is None \
                    or not status \
                    or not authors:
                error_count += 1
                logger.error(f"Недостаточно данных для добавления книги: {title} ({isbn})")
                continue

            author_objs = []
            for author_name in authors:
                author_obj, _ = Author.objects.get_or_create(name=author_name)
                author_objs.append(author_obj)

            category_objs = parse_categories(categories)

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

            for category_obj in category_objs:
                book_obj.categories.add(category_obj)

            if thumbnail_url:
                try:
                    temp_image = NamedTemporaryFile(delete=True)
                    temp_image.write(requests.get(thumbnail_url).content)
                    temp_image.flush()

                    image_name = os.path.basename(thumbnail_url)
                    content_file = ContentFile(temp_image.read(), name=image_name)

                    book_obj.cover_image.save(image_name, content_file)
                except Exception as e:
                    logger.error(f"Ошибка при загрузке обложки для книги {title} ({isbn}): {e}")

            book_obj.save()
            added_count += 1

        except Exception as e:
            error_count += 1
            logger.error(f"Ошибка при обработке книги: {e}")

    return {
        "Added": added_count,
        "Duplicates": duplicate_count,
        "Errors": error_count,
        "ReturnMessage": "Добавление книг прошло успешно."
    }
