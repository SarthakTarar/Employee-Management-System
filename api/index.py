"""
Vercel Python runtime entrypoint.

Vercel's @vercel/python builder looks for a WSGI-compatible callable named
`app` (or `handler`) in this module. We just expose Django's own WSGI
application here.
"""

import os
import sys
from pathlib import Path

# Make the project root importable (this file lives in api/, one level down).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "office_emp_m.settings")

from django.core.wsgi import get_wsgi_application  # noqa: E402

app = get_wsgi_application()
