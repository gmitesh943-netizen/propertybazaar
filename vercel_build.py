"""Vercel build: run DB migrations before deploy."""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from django.core.management import call_command

call_command("migrate", "--noinput", verbosity=1)
