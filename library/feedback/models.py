from django.db import models


class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=64)
    name = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField()
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.email

