from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q
import os
from .category_ancestors import get_category_ancestors
from .models import Category, Book, AppSettings
from .books_parse import parser
from .forms import BookSearchForm

DEFAULT_IMAGE_PATH = os.path.join(settings.BASE_DIR, 'media', 'default_image.jpg')


def index(request):
    top_level_categories = Category.objects.filter(parent=None)
    top_level_categories = sorted(top_level_categories, key=lambda category: category.name)

    context = {
        'top_level_categories': top_level_categories,
    }

    return render(request, 'books/index.html', context)


def category_detail(request, category_id):
    category = Category.objects.get(pk=category_id)
    ancestors = get_category_ancestors(category)
    subcategories = Category.objects.filter(parent=category)

    books = Book.objects.filter(categories=category)

    app_settings = AppSettings.objects.first()
    books_per_page = app_settings.books_per_page

    paginator = Paginator(books, books_per_page)
    page_number = request.GET.get('page')
    books_on_page = paginator.get_page(page_number)

    context = {
        'category': category,
        'ancestors': ancestors,
        'subcategories': subcategories,
        'books_on_page': books_on_page,
        'default_image': DEFAULT_IMAGE_PATH,
    }

    return render(request, 'books/category_detail.html', context)


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    category_path = get_category_ancestors(book.categories.last()) + [book.categories.last()]

    other_books_in_category = Book.objects.filter(categories=book.categories.last()).exclude(id=book_id)

    context = {
        'book': book,
        'ancestors': category_path,
        'default_image': DEFAULT_IMAGE_PATH,
        'other_books_in_category': other_books_in_category,
    }

    return render(request, 'books/book_detail.html', context)


def book_search(request):
    results = []
    show_results = False

    if request.method == 'GET':
        form = BookSearchForm(request.GET)
        if form.is_valid():
            query = Q()

            title = form.cleaned_data.get('title')
            if title:
                query &= Q(title__icontains=title)

            isbn = form.cleaned_data.get('isbn')
            if isbn:
                query &= Q(isbn__icontains=isbn)

            published_date_start = form.cleaned_data.get('published_date_start')
            if published_date_start:
                query &= Q(published_date__gte=published_date_start)

            published_date_end = form.cleaned_data.get('published_date_end')
            if published_date_end:
                query &= Q(published_date__lte=published_date_end)

            status = form.cleaned_data.get('status')
            if status:
                query &= Q(status=status)

            author_name = form.cleaned_data.get('author_name')
            if author_name:
                query &= Q(authors__name__icontains=author_name)

            if query:
                results = Book.objects.filter(query)
                show_results = True

    else:
        form = BookSearchForm()

    context = {
        'form': form,
        'results': results,
        'show_results': show_results,
    }

    return render(request, 'books/book_search.html', context)


@staff_member_required
def settings_view(request):
    report_settings = None
    app_settings = AppSettings.objects.first()

    if not app_settings:
        app_settings = AppSettings()
        app_settings.books_per_page = 20
        app_settings.feedback_email = "vi812x@gmail.com"
        app_settings.data_source_url = "https://gitlab.grokhotov.ru/hr/symfony-test-vacancy/-/raw/main/books.json"
        app_settings.save()

    if request.method == "POST":
        if "pagination_setting" in request.POST:
            app_settings.books_per_page = request.POST.get("books_per_page", app_settings.books_per_page)
            app_settings.save()
            report_settings = {"ReturnMessage": "Сохранение настроек пагинации прошло успешно."}

        elif "feedback_email_setting" in request.POST:
            app_settings.feedback_email = request.POST.get("feedback_email", app_settings.feedback_email)
            app_settings.save()
            report_settings = {"ReturnMessage": "Сохранение email прошло успешно."}

        elif "load_data_url" in request.POST:
            app_settings.data_source_url = request.POST.get("data_source_url", app_settings.data_source_url)
            report_settings = parser(app_settings.data_source_url)
            app_settings.save()

    context = {"app_settings": app_settings, "report_settings": report_settings}
    return render(request, "books/settings.html", context)
