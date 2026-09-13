#!/bin/bash
set -e

echo "Installing dependencies..."
# Vercel's static-build container ships a uv-managed Python (PEP 668:
# "externally-managed-environment") that refuses a plain `pip install`.
# This is an isolated, throwaway build container, not a shared system
# Python, so overriding that guard here is safe.
pip install --break-system-packages -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear
