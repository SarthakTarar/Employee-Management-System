from django.conf import settings
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

from .demo_data import reset_demo_database


def _is_demo_user(user):
    return bool(user and getattr(user, "username", None) == settings.DEMO_USERNAME)


@receiver(user_logged_in)
def reset_demo_on_login(sender, request, user, **kwargs):
    # Covers the case where the previous visitor never logged out cleanly.
    if _is_demo_user(user):
        reset_demo_database()


@receiver(user_logged_out)
def reset_demo_on_logout(sender, request, user, **kwargs):
    if _is_demo_user(user):
        reset_demo_database()
