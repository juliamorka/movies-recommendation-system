from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id = models.CharField(max_length=100, primary_key=True)
