import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from properties.models import Category, PropertyType, Amenity, Property, PropertyImage
from django.utils.text import slugify

User = get_user_model()

def seed_full_ahmedabad():
    # 1. Get or Create Admin User
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

    # 2. Get Categories and Types
    res_cat, _ = Category.objects.get_or_create(name='Residential')
    com_cat, _ = Category.objects.get_or_create(name='Commercial')
    
    apt_type, _ = PropertyType.objects.get_or_create(name='Apartment')
    villa_type, _ = PropertyType.objects.get_or_create(name='Villa')
    office_type, _ = PropertyType.objects.get_or_create(name='Office')
    shop_type, _ = PropertyType.objects.get_or_create(name='Shop')

    # 3. Amenities
    pool, _ = Amenity.objects.get_or_create(name='Swimming Pool', defaults={'icon': 'fa-swimming-pool'})
    gym, _ = Amenity.objects.get_or_create(name='Gym', defaults={'icon': 'fa-dumbbell'})
    parking, _ = Amenity.objects.get_or_create(name='Parking', defaults={'icon': 'fa-car'})
    security, _ = Amenity.objects.get_or_create(name='Security', defaults={'icon': 'fa-shield-alt'})
    garden, _ = Amenity.objects.get_or_create(name='Garden', defaults={'icon': 'fa-tree'})

    areas = [
        'Satellite', 'South Bopal', 'Gota', 'Prahlad Nagar', 'Vastrapur', 
        'Bodakdev', 'Science City', 'Chandkheda', 'Nikol', 'Naroda', 
        'Maninagar', 'Ambawadi', 'Ellisbridge', 'Navrangpura', 'Usmanpura',
        'Memnagar', 'Gurukul', 'Thaltej', 'Sola', 'Vaishno Devi Circle'
    ]

    property_titles = [
        'Luxury {} in {}', 'Spacious {} for {}', 'Elegant {} in heart of {}',
        'Modern {} with amenities in {}', 'Affordable {} in {}', 'Premium {} at {}'
    ]

    descriptions = [
        "Experience world-class living in this beautifully designed property located in {}. With state-of-the-art amenities and prime location, it's the perfect choice for you.",
        "A wonderful opportunity to own/rent a property in the bustling area of {}. Close to schools, hospitals, and shopping centers.",
        "Looking for a peaceful yet connected lifestyle? This property in {} offers exactly that. Spacious rooms and great ventilation."
    ]

    for i in range(1, 31):
        area = random.choice(areas)
        p_type = random.choice([apt_type, villa_type, office_type, shop_type])
        listing_type = random.choice(['sale', 'rent'])
        
        if listing_type == 'sale':
            if p_type == villa_type:
                price = random.randint(15000000, 50000000)
            elif p_type == office_type:
                price = random.randint(8000000, 30000000)
            else:
                price = random.randint(4000000, 15000000)
        else: # rent
            if p_type == villa_type:
                price = random.randint(40000, 120000)
            elif p_type == office_type:
                price = random.randint(25000, 80000)
            else:
                price = random.randint(15000, 45000)

        title = random.choice(property_titles).format(p_type.name, area)
        description = random.choice(descriptions).format(area)
        
        prop = Property.objects.create(
            owner=user,
            title=f"{title} #{i}",
            category=res_cat if p_type in [apt_type, villa_type] else com_cat,
            property_type=p_type,
            listing_type=listing_type,
            description=description,
            price=price,
            area=random.randint(800, 4000),
            bedrooms=random.randint(1, 5) if p_type in [apt_type, villa_type] else 0,
            bathrooms=random.randint(1, 4),
            rooms=random.randint(2, 8),
            address=f"Street {i}, {area}",
            city='Ahmedabad',
            state='Gujarat',
            zip_code=str(380000 + random.randint(1, 99)),
            featured=random.choice([True, False, False, False]),
            status='published'
        )
        
        prop.amenities.add(parking, security)
        if random.choice([True, False]):
            prop.amenities.add(garden)
        if prop.featured:
            prop.amenities.add(pool, gym)
            
        # Add random image from media if exists
        img_num = (i % 5) + 1
        img_path = f"property_images/{img_num}.png"
        PropertyImage.objects.create(property=prop, image=img_path)

    print(f"Successfully seeded 30 properties in Ahmedabad.")

if __name__ == '__main__':
    seed_full_ahmedabad()
