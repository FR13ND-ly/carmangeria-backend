from django.conf import settings
from django.db import models
from django.utils import timezone

class User(models.Model):
    username = models.CharField(max_length=64, unique=True)
    password = models.TextField()
    isAdmin = models.BooleanField(default=False)

class Token(models.Model):
    userId = models.PositiveIntegerField(null=True)
    token = models.TextField()
    date = models.DateTimeField(default=timezone.now)