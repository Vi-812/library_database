from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import AppSettings
from .books_parse import parser


@staff_member_required
def settings_view(request):
    app_settings = AppSettings.objects.first()

    if not app_settings:
        app_settings = AppSettings()
        app_settings.books_per_page = 20
        app_settings.feedback_email = "vi812x@gmail.com"
        app_settings.data_source_url = "https://gitlab.grokhotov.ru/hr/symfony-test-vacancy/-/raw/main/books.json"
        app_settings.save()

    if request.method == 'POST':
        app_settings.books_per_page = request.POST.get('books_per_page', app_settings.books_per_page)
        app_settings.feedback_email = request.POST.get('feedback_email', app_settings.feedback_email)
        app_settings.data_source_url = request.POST.get('data_source_url', app_settings.data_source_url)
        app_settings.save()

    if request.method == 'POST':
        if 'pagination_setting' in request.POST:
            app_settings.books_per_page = request.POST.get('books_per_page', app_settings.books_per_page)
        elif 'feedback_email_setting' in request.POST:
            app_settings.feedback_email = request.POST.get('feedback_email', app_settings.feedback_email)
        elif 'load_data_url' in request.POST:
            app_settings.data_source_url = request.POST.get('data_source_url', app_settings.data_source_url)
            parser(app_settings.data_source_url)

        app_settings.save()

    context = {'app_settings': app_settings}
    return render(request, 'settings.html', context)
