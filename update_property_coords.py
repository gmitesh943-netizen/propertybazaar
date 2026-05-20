import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from properties.models import Property

# Approximate coordinates for Ahmedabad areas
area_coords = {
    'Satellite': (23.0300, 72.5300),
    'South Bopal': (23.0100, 72.4700),
    'Gota': (23.1000, 72.5400),
    'Prahlad Nagar': (23.0100, 72.5100),
    'Vastrapur': (23.0300, 72.5200),
    'Bodakdev': (23.0400, 72.5100),
    'Science City': (23.0800, 72.5100),
    'Chandkheda': (23.1000, 72.5900),
    'Nikol': (23.0500, 72.6700),
    'Naroda': (23.0700, 72.6500),
    'Maninagar': (22.9900, 72.6000),
    'Ambawadi': (23.0200, 72.5500),
    'Ellisbridge': (23.0200, 72.5700),
    'Navrangpura': (23.0400, 72.5600),
    'Usmanpura': (23.0500, 72.5600),
    'Memnagar': (23.0500, 72.5300),
    'Gurukul': (23.0500, 72.5300),
    'Thaltej': (23.0500, 72.5000),
    'Sola': (23.0700, 72.5300),
    'Vaishno Devi Circle': (23.1300, 72.5500)
}

def update_property_coords():
    properties = Property.objects.filter(city__isnull=False)
    updated_count = 0
    
    for prop in properties:
        # Check if any area name is in the title or address or city field
        coords = None
        for area, latlng in area_coords.items():
            if area.lower() in prop.city.lower() or area.lower() in prop.address.lower() or area.lower() in prop.title.lower():
                coords = latlng
                break
        
        if coords:
            prop.latitude = coords[0]
            prop.longitude = coords[1]
            prop.save()
            updated_count += 1
            print(f"Updated: {prop.title} in {prop.city} -> {coords}")
        else:
            # Default to Ahmedabad center if no area match
            prop.latitude = 23.0225
            prop.longitude = 72.5714
            prop.save()
            print(f"Default coords for: {prop.title}")

    print(f"Successfully updated coordinates for {updated_count} properties.")

if __name__ == '__main__':
    update_property_coords()
