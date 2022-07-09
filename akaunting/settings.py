from django.conf import settings
from rest_framework.settings import perform_import

IMPORT_STRINGS = [
    "PAYMENT_ATTACHMENT_UPLOAD_TO",
]

AKAUNTING_DEFAULTS = {
    "PAYMENT_ATTACHMENT_UPLOAD_TO": "akaunting.purchases.payments.upload_to._payment_upload_to",  # noqa E501
    "PAYMENT_MODEL_ABSTRACT": False,
}


class AppSettings:
    """
    Inspired from DRF
    """

    def __init__(self, user_settings, defaults, import_strings=None):
        self._user_settings = user_settings
        self.defaults = defaults
        self.import_strings = import_strings or []

    @property
    def user_settings(self):
        return getattr(settings, self._user_settings, {})

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid setting: '%s'" % attr)  # pragma: no cover

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Coerce import strings into classes
        if attr in self.import_strings:
            val = perform_import(val, attr)

        return val


akaunting_settings = AppSettings(
    user_settings="AKAUNTING_SETTINGS",
    defaults=AKAUNTING_DEFAULTS,
    import_strings=IMPORT_STRINGS,
)
