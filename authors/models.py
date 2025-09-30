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
    
    favorite_authors = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='favorited_by',
        blank=True
    )

    def __str__(self):
        return self.username


class Notifications(models.Model):
    recipient = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.message[:20]}"