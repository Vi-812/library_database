from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import Category, Book, AppSettings
from .books_parse import parser


def index(request):
    top_level_categories = Category.objects.filter(parent=None)

    books_without_categories = Book.objects.filter(categories=None)

    context = {
        'top_level_categories': top_level_categories,
        'books_without_categories': books_without_categories
    }

    return render(request, 'index.html', context)


def category_detail(request, category_id):
    category = Category.objects.get(pk=category_id)

    context = {
        'category': category,
    }

    return render(request, 'category_detail.html', context)


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
    return render(request, "settings.html", context)
