import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from properties.models import Category, PropertyType, Amenity

def seed_data():
    # Categories
    categories = ['Residential', 'Commercial', 'Industrial', 'Land']
    for cat in categories:
        Category.objects.get_or_create(name=cat)
    print("Categories seeded.")

    # Property Types
    types = ['Apartment', 'Villa', 'House', 'Office', 'Shop', 'Warehouse', 'Plot']
    for t in types:
        PropertyType.objects.get_or_create(name=t)
    print("Property Types seeded.")

    # Amenities
    amenities = [
        ('Swimming Pool', 'fa-swimming-pool'),
        ('Gym', 'fa-dumbbell'),
        ('Parking', 'fa-car'),
        ('Security', 'fa-shield-alt'),
        ('Garden', 'fa-tree'),
        ('Elevator', 'fa-elevator'),
    ]
    for name, icon in amenities:
        Amenity.objects.get_or_create(name=name, icon=icon)
    print("Amenities seeded.")

if __name__ == '__main__':
    seed_data()
