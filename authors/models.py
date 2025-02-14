from django.contrib.auth.models import AbstractUser
from django.db import models


class Author(AbstractUser):

    age = models.PositiveIntegerField(blank=False, null=False)
    gender = models.CharField(
        max_length=225,
        choices=[("male", "Male"), ("female", "Female")],
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.username
