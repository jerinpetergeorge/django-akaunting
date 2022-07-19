from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from akaunting.settings import akaunting_settings


class Customer(TimeStampedModel):
    name = models.CharField(_("Name"), max_length=100)

    class Meta:
        abstract = "Customer" in akaunting_settings.ABSTRACT_MODELS
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")
        db_table = "Customer"

    def __str__(self):
        return self.name
