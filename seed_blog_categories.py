import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from blog.models import Category


categories = [
    {'name': 'Latest Blogs', 'slug': 'latest-blogs', 'icon': 'fas fa-newspaper'},
    {'name': 'Lifestyle', 'slug': 'lifestyle', 'icon': 'fas fa-couch'},
    {'name': 'Policies', 'slug': 'policies', 'icon': 'fas fa-file-contract'},
    {'name': 'Finance & Legal', 'slug': 'finance-legal', 'icon': 'fas fa-balance-scale'},
    {'name': 'City Blogs', 'slug': 'city-blogs', 'icon': 'fas fa-city'},
    {'name': 'Property News', 'slug': 'property-news', 'icon': 'fas fa-home'},
    {'name': 'Trending Web Stories', 'slug': 'trending-web-stories', 'icon': 'fas fa-bolt'},
]

for cat_data in categories:
    cat, created = Category.objects.get_or_create(
        slug=cat_data['slug'],
        defaults={'name': cat_data['name'], 'icon': cat_data['icon']}
    )
    if created:
        print(f"Created category: {cat.name}")
    else:
        print(f"Category already exists: {cat.name}")
