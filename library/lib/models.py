from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    publication_year = models.IntegerField()
    isbn = models.CharField(max_length=13)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
   username = models.CharField(max_length=150, unique=True)
   password = models.CharField(max_length=128)
   email = models.EmailField(unique=True)
   confirm_password = models.CharField(max_length=128)

def __str__(self):
        return self.username

