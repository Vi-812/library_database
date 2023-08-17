from django import forms
from django.forms import widgets
from .models import Book, Author, Category


class BookSearchForm(forms.Form):
    title = forms.CharField(label='Название', required=False)
    isbn = forms.CharField(label='ISBN', required=False)
    published_date_start = forms.DateField(
        label='Дата публикации с',
        required=False,
        widget=widgets.DateInput(attrs={'type': 'date'}),
    )
    published_date_end = forms.DateField(
        label='Дата публикации по',
        required=False,
        widget=widgets.DateInput(attrs={'type': 'date'}),
    )
    status = forms.ChoiceField(label='Статус', choices=[], required=False)
    author_name = forms.CharField(label='Имя автора', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = [('', '---------')] + list(Book.objects.values_list('status', 'status').distinct())
        self.fields['status'].initial = None
