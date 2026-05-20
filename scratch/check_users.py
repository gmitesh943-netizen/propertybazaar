import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User

users = User.objects.all()
print(f"Total users: {users.count()}")
for user in users:
    print(f"Email: {user.email}, Role: {user.role}, Is Active: {user.is_active}, Is Verified: {user.is_verified}")
