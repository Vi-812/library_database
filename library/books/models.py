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
    isbn = models.CharField(max_length=20)
    pages = models.IntegerField()
    published_date = models.DateField()
    thumbnail_url = models.URLField()
    cover_image = models.ImageField(upload_to='book_covers/', null=True)
    short_description = models.TextField()
    long_description = models.TextField()
    status = models.CharField(max_length=10)

    authors = models.ManyToManyField(Author)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title


class AppSettings(models.Model):
    books_per_page = models.PositiveIntegerField(default=20)
    feedback_email = models.EmailField(default="vi812x@gmail.com")
    data_source_url = models.URLField(
        default="https://gitlab.grokhotov.ru/hr/symfony-test-vacancy/-/raw/main/books.json")
