from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from akaunting.settings import akaunting_settings


class Organization(TimeStampedModel):
    name = models.CharField(_("Name"), max_length=100)
    email = models.EmailField(_("Email"), unique=True)

    class Meta:
        abstract = "Organization" in akaunting_settings.ABSTRACT_MODELS
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")
        db_table = "Organization"
        ordering = ["name"]

    def __str__(self):
        return self.name
