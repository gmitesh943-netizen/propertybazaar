"""Vercel build: run DB migrations before deploy."""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from django.core.management import call_command

if os.environ.get("DATABASE_URL"):
    call_command("migrate", "--noinput", verbosity=1)
else:
    print("Skip migrate: set DATABASE_URL in Vercel Environment Variables (Neon.tech)")
