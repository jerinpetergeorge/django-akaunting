from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel


class Category(TimeStampedModel):
    name = models.CharField(_("Name"), max_length=50)
    description = models.TextField(_("Description"), blank=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        db_table = "Category"

    def __str__(self):
        return self.name
