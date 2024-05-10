from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    librarian_id = models.CharField(
        max_length=8, primary_key=True, unique=True)
    email = models.EmailField(max_length=200, unique=True)
