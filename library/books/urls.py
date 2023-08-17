from django.urls import path
from .views import *

app_name = 'books'

urlpatterns = [
    path('', index, name='index'),
    path('category/<int:category_id>/', category_detail, name='category_detail'),
    path('book/<int:book_id>/', book_detail, name='book_detail'),
    path('search/', book_search, name='book_search'),
    path('settings/', settings_view, name='app_settings'),
]
