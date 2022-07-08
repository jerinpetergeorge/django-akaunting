from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel


class Vendor(TimeStampedModel):
    name = models.CharField(_("Name"), max_length=50)

    class Meta:
        verbose_name = _("Vendor")
        verbose_name_plural = _("Vendors")
        db_table = "Vendor"
        ordering = ["name"]

    def __str__(self):
        return self.name
