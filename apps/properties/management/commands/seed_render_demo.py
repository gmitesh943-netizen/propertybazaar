"""Seed demo properties with Unsplash image URLs for Render (no local media folder)."""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from properties.models import Category, PropertyType, Property, PropertyImage

User = get_user_model()

UNSPLASH = [
    'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80',
    'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=1200&q=80',
    'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1200&q=80',
    'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80',
    'https://images.unsplash.com/photo-1545324418-f1d3ac157359?auto=format&fit=crop&w=1200&q=80',
    'https://images.unsplash.com/photo-1613490493576-7fde63acd811?auto=format&fit=crop&w=1200&q=80',
]

DEMO_PROPERTIES = [
    {
        'title': 'Luxurious 4 BHK Apartment in Satellite',
        'price': 18500000,
        'area': 2800,
        'bedrooms': 4,
        'bathrooms': 4,
        'city': 'Ahmedabad',
        'featured': True,
        'img': 0,
    },
    {
        'title': 'Modern 3 BHK Flat in Bopal',
        'price': 7500000,
        'area': 1650,
        'bedrooms': 3,
        'bathrooms': 3,
        'city': 'Ahmedabad',
        'featured': True,
        'img': 1,
    },
    {
        'title': 'Spacious 5 BHK Villa in Gota',
        'price': 25000000,
        'area': 4500,
        'bedrooms': 5,
        'bathrooms': 5,
        'city': 'Ahmedabad',
        'featured': True,
        'img': 2,
    },
    {
        'title': 'Premium 2 BHK in Prahlad Nagar',
        'price': 6500000,
        'area': 1250,
        'bedrooms': 2,
        'bathrooms': 2,
        'city': 'Ahmedabad',
        'featured': True,
        'img': 3,
    },
]


class Command(BaseCommand):
    help = 'Seed properties with online image URLs for production (Render)'

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            email='admin@propertybazaar.com',
            defaults={
                'first_name': 'Admin',
                'last_name': 'User',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
            },
        )
        if created:
            user.set_password('admin123')
            user.save()

        res_cat, _ = Category.objects.get_or_create(name='Residential')
        apt_type, _ = PropertyType.objects.get_or_create(name='Apartment')

        # Fix existing images missing files on server
        fixed = 0
        for pi in PropertyImage.objects.all():
            has_file = bool(pi.image) and pi.image.storage.exists(pi.image.name)
            if not has_file and not pi.image_url:
                pi.image_url = UNSPLASH[pi.id % len(UNSPLASH)]
                pi.save(update_fields=['image_url'])
                fixed += 1
        if fixed:
            self.stdout.write(f'Fixed {fixed} broken property images with URLs')

        for i, data in enumerate(DEMO_PROPERTIES):
            img_idx = data.pop('img')
            prop, created = Property.objects.get_or_create(
                title=data['title'],
                defaults={
                    **data,
                    'owner': user,
                    'status': 'published',
                    'category': res_cat,
                    'property_type': apt_type,
                    'address': 'Ahmedabad',
                    'state': 'Gujarat',
                    'zip_code': '380001',
                    'description': f"Premium property in {data['city']}.",
                    'slug': slugify(data['title']),
                },
            )
            if created or not prop.images.exists():
                PropertyImage.objects.filter(property=prop).delete()
                PropertyImage.objects.create(
                    property=prop,
                    image_url=UNSPLASH[img_idx % len(UNSPLASH)],
                    is_featured=True,
                )
                self.stdout.write(self.style.SUCCESS(f'Seeded: {prop.title}'))

        self.stdout.write(self.style.SUCCESS('Render demo seed complete'))
