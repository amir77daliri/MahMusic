from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_singer = models.BooleanField(default=False, blank=True)

    def __str__(self):
        if self.first_name and self.last_name:
            return self.get_full_name()
        return self.username

