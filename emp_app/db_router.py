"""
Routes emp_app's models to a separate "demo" database for whichever request
is currently flagged as a demo request (see middleware.py, which sets the
flag based on the logged-in username). Every other app (auth, sessions,
admin, ...) always stays on "default" — only the employee/department/role
data needs a second, disposable copy for the public demo account.
"""

import threading

_state = threading.local()

DEMO_ROUTED_APPS = {"emp_app"}


def set_demo_active(active):
    _state.active = active


def is_demo_active():
    return getattr(_state, "active", False)


class DemoRouter:
    def _alias_for(self, model):
        if is_demo_active() and model._meta.app_label in DEMO_ROUTED_APPS:
            return "demo"
        return None

    def db_for_read(self, model, **hints):
        return self._alias_for(model)

    def db_for_write(self, model, **hints):
        return self._alias_for(model)

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == "demo":
            return app_label in DEMO_ROUTED_APPS
        return True
