import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = (
        "Creates (or resets the password of) the public demo account. "
        "Reads DEMO_USER_PASSWORD from the environment, or --password."
    )

    def add_arguments(self, parser):
        parser.add_argument("--username", default=None)
        parser.add_argument("--password", default=None)

    def handle(self, *args, **options):
        User = get_user_model()

        from django.conf import settings

        username = options["username"] or settings.DEMO_USERNAME
        password = options["password"] or os.environ.get("DEMO_USER_PASSWORD")
        if not password:
            raise CommandError(
                "Set DEMO_USER_PASSWORD in the environment or pass --password."
            )

        user, created = User.objects.get_or_create(username=username)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.is_active = True
        user.save()

        verb = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"{verb} demo account '{username}'."))
