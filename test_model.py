import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

try:
    from properties.models import Builder
    print("Builder model exists!")
except ImportError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Other error: {e}")
