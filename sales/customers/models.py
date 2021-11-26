from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel


class Customer(TimeStampedModel):
    name = models.CharField(_("Name"), max_length=100)

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")
        db_table = "Customer"

    def __str__(self):
        return self.name
