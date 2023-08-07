from django.urls import path
from .views import settings_view

app_name = 'books'

urlpatterns = [
    path('', settings_view, name='index'),
    path('settings/', settings_view, name='app_settings'),
]
