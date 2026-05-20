import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from properties.models import Builder

builders_data = [
    {
        "name": "OMAXE",
        "stat1_value": "124.3 Mn sqft",
        "stat1_label": "Delivered projects till date",
        "stat2_value": "150,000+",
        "stat2_label": "Happy families",
        "leader_name": "Mohit Goel",
        "leader_designation": "CEO, Omaxe Limited",
    },
    {
        "name": "VTP REALTY",
        "stat1_value": "300+ homes",
        "stat1_label": "Selling Every Month",
        "stat2_value": "35 Lakh+ sqft",
        "stat2_label": "Delivered",
        "leader_name": "Sachin Bhandari",
        "leader_designation": "CEO, VTP Realty",
    },
    {
        "name": "SPR CITY",
        "stat1_value": "63 acres",
        "stat1_label": "Integrated township",
        "stat2_value": "75+",
        "stat2_label": "Amenities",
        "leader_name": "Navin Ranka",
        "leader_designation": "Director, SPR Group",
    }
]

for data in builders_data:
    builder, created = Builder.objects.get_or_create(
        name=data["name"],
        defaults={
            "stat1_value": data["stat1_value"],
            "stat1_label": data["stat1_label"],
            "stat2_value": data["stat2_value"],
            "stat2_label": data["stat2_label"],
            "leader_name": data["leader_name"],
            "leader_designation": data["leader_designation"],
            "created_at": timezone.now()
        }
    )
    if created:
        print(f"Created builder: {builder.name}")
    else:
        print(f"Builder {builder.name} already exists.")
