import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from properties.models import Property

# Ahmedabad hotspot center coordinates with small random offsets to spread properties realistically
LOCATION_COORDS = {
    'Vaishnodevi-Gota-Zundal': (23.0860, 72.5320),
    'Chandkheda':               (23.1050, 72.5890),
    'Bopal & South Bopal':      (23.0310, 72.4700),
    'Naroda':                   (23.0850, 72.6450),
    'Rest of Ahmedabad':        (23.0225, 72.5714),
    'Ahmedabad':                (23.0225, 72.5714),
}

updated = 0
for prop in Property.objects.all():
    matched = False
    for location_name, (lat, lng) in LOCATION_COORDS.items():
        if location_name.lower() in prop.title.lower():
            # Add small random offset within ~1km so properties don't stack
            prop.latitude  = round(lat + random.uniform(-0.008, 0.008), 6)
            prop.longitude = round(lng + random.uniform(-0.008, 0.008), 6)
            prop.save()
            print(f"Updated '{prop.title}' -> ({prop.latitude}, {prop.longitude})")
            updated += 1
            matched = True
            break
    if not matched and not prop.latitude:
        # Default to Ahmedabad city center
        prop.latitude  = round(23.0225 + random.uniform(-0.01, 0.01), 6)
        prop.longitude = round(72.5714 + random.uniform(-0.01, 0.01), 6)
        prop.save()
        print(f"Defaulted '{prop.title}' -> ({prop.latitude}, {prop.longitude})")
        updated += 1

print(f"\nDone! Updated {updated} properties with coordinates.")
