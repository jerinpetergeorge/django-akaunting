from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from .default import default_webhook_secret


class Event(TimeStampedModel):
    name = models.CharField(_("Name"), max_length=50)
    enabled = models.BooleanField(_("Enabled"), default=True)

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        db_table = "Event"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Webhook(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        related_name="webhooks",
        related_query_name="webhook",
        verbose_name=_("User"),
    )
    nickname = models.CharField(_("Nick Name"), max_length=50)
    secret = models.CharField(
        _("Webhook Secret"),
        max_length=100,
        default=default_webhook_secret,
    )
    url = models.URLField(_("Target URL"))
    events = models.ManyToManyField("Event")
    enabled = models.BooleanField(_("Enabled"), default=True)

    class Meta:
        verbose_name = _("Webhook")
        verbose_name_plural = _("Webhooks")
        db_table = "Webhook"
        ordering = ["-created"]

    def __str__(self):
        return self.nickname
