from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand, call_command

User = get_user_model()


class Command(BaseCommand):
    help = "Restore local environment and install minimal items"

    def create_superuser(self):
        User.objects.create_superuser(
            settings.DEV_EMAIL, settings.DEV_PASSWORD, full_name=settings.DEV_FULL_NAME
        )

    def handle(self, *args, **options):
        call_command("reset_db", "--noinput")
        call_command("migrate")
        self.create_superuser()
        self.stdout.write(self.style.SUCCESS("Restore Completed!!!"))
