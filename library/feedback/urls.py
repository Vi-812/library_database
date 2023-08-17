from django.urls import path
from .views import feedback_view

app_name = 'feedback'

urlpatterns = [
    path('feedback/', feedback_view, name='feedback'),
]
