import typing

from django.conf import settings

if typing.TYPE_CHECKING:
    from .models import Payment


def _payment_upload_to(instance: "Payment", filename: str):
    return f"{settings.MEDIA_ROOT}{instance.user_id}/payment/{filename}"
