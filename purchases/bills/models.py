from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel


class Bill(TimeStampedModel):
    class Meta:
        verbose_name = _("Bill")
        verbose_name_plural = _("Bills")
        db_table = "Bill"
