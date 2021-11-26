from django.contrib.auth.models import AbstractUser
from django.db import models

from .manager import UserManager


class User(AbstractUser):
    first_name = None
    last_name = None
    username = None

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    is_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "User"

    def __str__(self):
        return f"{self.full_name} ({self.email})"
