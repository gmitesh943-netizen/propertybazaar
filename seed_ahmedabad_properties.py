import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from properties.models import Category, PropertyType, Amenity, Property, PropertyImage
from django.utils.text import slugify

User = get_user_model()

def seed_ahmedabad_properties():
    # 1. Get or Create User
    user, created = User.objects.get_or_create(
        email='admin@propertybazaar.com',
        defaults={
            'first_name': 'Admin',
            'last_name': 'User',
            'role': 'admin',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        user.set_password('admin123')
        user.save()
        print("Admin user created.")

    # 2. Get Categories and Types
    res_cat, _ = Category.objects.get_or_create(name='Residential')
    com_cat, _ = Category.objects.get_or_create(name='Commercial')
    
    apt_type, _ = PropertyType.objects.get_or_create(name='Apartment')
    villa_type, _ = PropertyType.objects.get_or_create(name='Villa')
    office_type, _ = PropertyType.objects.get_or_create(name='Office')

    # 3. Get Amenities
    pool, _ = Amenity.objects.get_or_create(name='Swimming Pool', defaults={'icon': 'fa-swimming-pool'})
    gym, _ = Amenity.objects.get_or_create(name='Gym', defaults={'icon': 'fa-dumbbell'})
    parking, _ = Amenity.objects.get_or_create(name='Parking', defaults={'icon': 'fa-car'})
    security, _ = Amenity.objects.get_or_create(name='Security', defaults={'icon': 'fa-shield-alt'})

    # 4. Property Data
    ahmedabad_properties = [
        {
            'title': 'Luxurious 4 BHK Apartment in Satellite',
            'price': 18500000,
            'area': 2800,
            'bedrooms': 4,
            'bathrooms': 4,
            'rooms': 6,
            'address': 'Satellite Cross Road',
            'city': 'Ahmedabad',
            'state': 'Gujarat',
            'zip_code': '380015',
            'category': res_cat,
            'property_type': apt_type,
            'description': 'A premium 4 BHK apartment with modern amenities in the heart of Satellite.',
            'featured': True,
            'images': ['property_images/1.png', 'property_images/2.png']
        },
        {
            'title': 'Modern 3 BHK Flat in Bopal',
            'price': 7500000,
            'area': 1650,
            'bedrooms': 3,
            'bathrooms': 3,
            'rooms': 5,
            'address': 'South Bopal',
            'city': 'Ahmedabad',
            'state': 'Gujarat',
            'zip_code': '380058',
            'category': res_cat,
            'property_type': apt_type,
            'description': 'Beautifully designed 3 BHK flat in a serene location of South Bopal.',
            'featured': False,
            'images': ['property_images/3.png']
        },
        {
            'title': 'Spacious 5 BHK Villa in Gota',
            'price': 25000000,
            'area': 4500,
            'bedrooms': 5,
            'bathrooms': 5,
            'rooms': 8,
            'address': 'S.G. Highway, Gota',
            'city': 'Ahmedabad',
            'state': 'Gujarat',
            'zip_code': '382481',
            'category': res_cat,
            'property_type': villa_type,
            'description': 'An independent 5 BHK villa with private garden and pool access.',
            'featured': True,
            'images': ['property_images/4.png', 'property_images/5.png']
        },
        {
            'title': 'Commercial Office Space in Prahlad Nagar',
            'price': 12000000,
            'area': 1200,
            'bedrooms': 0,
            'bathrooms': 2,
            'rooms': 3,
            'address': 'Corporate Road, Prahlad Nagar',
            'city': 'Ahmedabad',
            'state': 'Gujarat',
            'zip_code': '380015',
            'category': com_cat,
            'property_type': office_type,
            'description': 'Prime office space suitable for IT companies and startups.',
            'featured': False,
            'images': ['property_images/El_13_de_septiembre_se_le_rinde_homenaje_a_uno_de.jpeg']
        },
        {
            'title': 'Budget 2 BHK Apartment in Nikol',
            'price': 4500000,
            'area': 1100,
            'bedrooms': 2,
            'bathrooms': 2,
            'rooms': 4,
            'address': 'Nikol-Naroda Road',
            'city': 'Ahmedabad',
            'state': 'Gujarat',
            'zip_code': '382350',
            'category': res_cat,
            'property_type': apt_type,
            'description': 'Affordable 2 BHK apartment for small families.',
            'featured': False,
            'images': []
        }
    ]

    # 5. Create Properties
    for p_data in ahmedabad_properties:
        images_data = p_data.pop('images')
        p_data['owner'] = user
        p_data['status'] = 'published'
        
        prop, created = Property.objects.get_or_create(
            title=p_data['title'],
            defaults=p_data
        )
        
        if created:
            prop.amenities.add(parking, security)
            if p_data['featured']:
                prop.amenities.add(pool, gym)
            
            # Add images
            for img_path in images_data:
                PropertyImage.objects.create(property=prop, image=img_path)
            
            print(f"Property created: {prop.title}")
        else:
            print(f"Property already exists: {prop.title}")

if __name__ == '__main__':
    seed_ahmedabad_properties()
