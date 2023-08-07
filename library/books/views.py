from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import AppSettings


@staff_member_required
def settings_view(request):
    app_settings = AppSettings.objects.first()

    if request.method == 'POST':
        app_settings.books_per_page = request.POST.get('books_per_page', app_settings.books_per_page)
        app_settings.feedback_email = request.POST.get('feedback_email', app_settings.feedback_email)
        app_settings.data_source_url = request.POST.get('data_source_url', app_settings.data_source_url)
        app_settings.save()

    context = {'app_settings': app_settings}
    return render(request, 'settings.html', context)
