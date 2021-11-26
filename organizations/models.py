from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel


class Organization(TimeStampedModel):
    name = models.CharField(_("name"), max_length=100)
    email = models.EmailField(_("email"), unique=True)

    def __str__(self):
        return self.name
