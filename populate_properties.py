import os
import sys
from pathlib import Path

# Add apps directory to sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / 'apps'))

import django
import urllib.request
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from django.utils.text import slugify

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from properties.models import Property, PropertyType, Category, PropertyImage

User = get_user_model()
agent = User.objects.filter(role='agent').first()

if not agent:
    print("No agent found!")
    exit()

locations = [
    'Vaishnodevi-Gota-Zundal',
    'Chandkheda',
    'Bopal & South Bopal',
    'Naroda',
    'Rest of Ahmedabad'
]

configs = [
    {'type': 'Apartment', 'cat': 'Residential', 'price': 15000, 'url': 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&q=80', 'title_prefix': 'Modern Flat in'},
    {'type': 'Villa', 'cat': 'Residential', 'price': 45000, 'url': 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&q=80', 'title_prefix': 'Luxury Villa in'},
    {'type': 'Office', 'cat': 'Commercial', 'price': 25000, 'url': 'https://images.unsplash.com/photo-1497366216548-37526070297c?w=800&q=80', 'title_prefix': 'Premium Workspace in'},
    {'type': 'Shop', 'cat': 'Commercial', 'price': 30000, 'url': 'https://images.unsplash.com/photo-1534452203293-494d7ddbf7e0?w=800&q=80', 'title_prefix': 'Retail Storefront in'}
]

print(f"Creating properties for agent: {agent.email}")

for loc in locations:
    for conf in configs:
        ptype = PropertyType.objects.get(name__icontains=conf['type'])
        pcat = Category.objects.get(name__icontains=conf['cat'])
        
        title = f"{conf['title_prefix']} {loc}"
        
        prop = Property.objects.create(
            owner=agent,
            title=title,
            category=pcat,
            property_type=ptype,
            listing_type='rent',
            description=f"This is a fantastic {conf['type'].lower()} available for rent in the prime location of {loc}. It offers great amenities and excellent connectivity.",
            price=conf['price'],
            area=1200 if conf['cat'] == 'Residential' else 800,
            bedrooms=2 if conf['cat'] == 'Residential' else 0,
            bathrooms=2 if conf['cat'] == 'Residential' else 1,
            rooms=3 if conf['cat'] == 'Residential' else 1,
            address=f"123 Main Street, {loc}",
            city="Ahmedabad",
            state="Gujarat",
            zip_code="380001",
            status='published'
        )
        
        print(f"Created property: {prop.title}")
        
        # Download and attach image
        try:
            req = urllib.request.Request(conf['url'], headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req)
            image_data = response.read()
            
            img_name = f"{slugify(title)}.jpg"
            
            p_img = PropertyImage(property=prop)
            p_img.image.save(img_name, ContentFile(image_data))
            p_img.save()
            print(f"  -> Added image {img_name}")
        except Exception as e:
            print(f"  -> Failed to add image: {e}")

print("Done generating properties!")
