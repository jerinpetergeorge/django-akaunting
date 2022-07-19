from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from akaunting.settings import akaunting_settings


class Payment(TimeStampedModel):
    class PaymentMethod(models.TextChoices):
        CASH = "cash", _("Cash")
        BANK_TRANSFER = "bank_transfer", _("Bank Transfer")

    item = models.CharField(_("Item"), max_length=250)
    amount = models.FloatField(_("Amount"))
    date = models.DateField(_("Date"))
    description = models.TextField(_("Description"), blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        related_name="payments",
        related_query_name="payment",
        verbose_name=_("User"),
    )
    vendor = models.ForeignKey(
        "vendors.Vendor",
        on_delete=models.CASCADE,
        related_name="payments",
        related_query_name="payment",
        verbose_name=_("Vendor"),
    )
    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.CASCADE,
        related_name="payments",
        related_query_name="payment",
        verbose_name=_("Category"),
    )
    payment_method = models.CharField(
        max_length=25,
        choices=PaymentMethod.choices,
        default=PaymentMethod.BANK_TRANSFER,
    )
    attachment = models.FileField(
        _("Attachment"),
        upload_to=akaunting_settings.PAYMENT_ATTACHMENT_UPLOAD_TO,
        blank=True,
    )
    extra_args = models.JSONField(
        _("Extra Arguments"),
        default=dict,
        blank=True,
    )

    class Meta:
        abstract = "Payment" in akaunting_settings.ABSTRACT_MODELS
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")
        db_table = "Payment"
        ordering = ["-date"]

    def __str__(self):
        return f"Paid {self.amount} to {self.vendor} on {self.date}"
