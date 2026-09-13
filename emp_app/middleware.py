from django.conf import settings

from .db_router import set_demo_active


class DemoDatabaseMiddleware:
    """
    Must sit after AuthenticationMiddleware (request.user must be resolved).
    Flags the current thread as "demo" for the duration of this request only
    when the logged-in user is the public demo account, so DemoRouter can
    route emp_app queries to the isolated demo database.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        is_demo = bool(
            user
            and user.is_authenticated
            and user.get_username() == settings.DEMO_USERNAME
        )
        set_demo_active(is_demo)
        try:
            response = self.get_response(request)
        finally:
            set_demo_active(False)
        return response
