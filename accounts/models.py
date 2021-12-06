from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .manager import UserManager


class User(AbstractUser):
    first_name = None
    last_name = None
    username = None

    email = models.EmailField(_("Email"), unique=True)
    full_name = models.CharField(_("Full Name"), max_length=150)
    is_verified = models.BooleanField(_("Is Verified?"), default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "User"

    def __str__(self):
        return f"{self.full_name} ({self.email})"
