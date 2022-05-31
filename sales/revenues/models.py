from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel


def _revenue_upload_to(instance: "Revenue", filename: str):
    return f"{settings.MEDIA_ROOT}{instance.user_id}/revenue/{filename}"


class Revenue(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        related_name="revenues",
        related_query_name="revenue",
        verbose_name=_("User"),
    )
    amount = models.FloatField(_("Amount"))
    date = models.DateField(_("Date"))
    description = models.TextField(_("Description"), blank=True)
    customer = models.ForeignKey(
        "customers.Customer",
        on_delete=models.CASCADE,
        related_name="revenues",
        related_query_name="revenue",
        verbose_name=_("Customer"),
    )
    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.CASCADE,
        related_name="revenues",
        related_query_name="revenue",
        verbose_name=_("Category"),
    )
    attachment = models.FileField(
        _("Attachment"),
        upload_to=_revenue_upload_to,
        blank=True,
    )

    class Meta:
        verbose_name = _("Revenue")
        verbose_name_plural = _("Revenues")
        db_table = "Revenues"

    def __str__(self):
        return f"Revenue(${self.amount} from {self.customer})"
