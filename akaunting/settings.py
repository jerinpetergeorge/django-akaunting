from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from rest_framework.settings import perform_import

IMPORT_STRINGS = [
    "PAYMENT_ATTACHMENT_UPLOAD_TO",
]

AKAUNTING_DEFAULTS = {
    "PAYMENT_ATTACHMENT_UPLOAD_TO": "akaunting.purchases.payments.upload_to._payment_upload_to",  # noqa E501
    "ABSTRACT_MODELS": [],
    "DISABLED_ADMINS": [],
}


def validate_disabled_admins(app_settings: "AppSettings"):
    for model_name in app_settings.ABSTRACT_MODELS:
        if model_name not in app_settings.DISABLED_ADMINS:
            raise ImproperlyConfigured(
                (
                    f"'{model_name}' is an abstract class, you "
                    f"need to disable it by adding to 'DISABLED_ADMINS'"
                ),
            )


class AppSettings:
    """
    Inspired from DRF
    """

    validators = [
        validate_disabled_admins,
    ]

    def __init__(self, user_settings, defaults, import_strings=None):
        self._user_settings = user_settings
        self.defaults = defaults
        self.import_strings = import_strings or []
        self._pre_validate()

    def _pre_validate(self):
        for validator in self.validators:
            validator(self)

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
