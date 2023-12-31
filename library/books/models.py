from django.db import models


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20, null=True, blank=True)
    page_count = models.IntegerField()
    published_date = models.DateField(null=True, blank=True)
    thumbnail_url = models.URLField(null=True, blank=True)
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    short_description = models.TextField(null=True, blank=True)
    long_description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10)

    authors = models.ManyToManyField(Author)
    categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.title


class AppSettings(models.Model):
    books_per_page = models.PositiveIntegerField(default=20)
    feedback_email = models.EmailField(default="vi812x@gmail.com")
    data_source_url = models.URLField(
        default="https://gitlab.grokhotov.ru/hr/symfony-test-vacancy/-/raw/main/books.json")
