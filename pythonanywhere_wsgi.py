# =====================================================================
# PythonAnywhere WSGI Configuration File for PropertyBazaar
# =====================================================================
# INSTRUCTIONS:
# 1. Go to Web Tab on PythonAnywhere
# 2. Click on WSGI Configuration File link
# 3. DELETE everything in that file
# 4. PASTE the content below (replacing YOUR_USERNAME with your actual username)
# =====================================================================

import os
import sys

# Replace 'YOUR_USERNAME' with your actual PythonAnywhere username
path = "/home/YOUR_USERNAME/propertybazaar"
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
