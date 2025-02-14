from django.db import models

from authors.models import Author


class Book(models.Model):
    title = models.CharField(max_length=70, blank=False, null=False)
    desc = models.TextField(blank=False, null=False)
    published_date = models.DateField()
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="Book_author"
    )
    updated_date = models.DateTimeField(auto_now=True)
    published_date_site = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False
    )
    category = models.CharField(max_length=70, blank=False, null=False)
