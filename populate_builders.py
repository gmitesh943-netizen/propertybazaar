import os
import sys
from pathlib import Path

# Add apps directory to sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / 'apps'))

import django
import requests
from django.core.files import File
from tempfile import NamedTemporaryFile

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from properties.models import Builder

def download_image(url):
    r = requests.get(url)
    if r.status_code == 200:
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(r.content)
        img_temp.flush()
        return img_temp
    return None

builders_data = [
    {
        "name": "OMAXE",
        "logo_url": "https://logowik.com/content/uploads/images/omaxe-limited5703.jpg",
        "stat1_value": "124.3 Mn sqft",
        "stat1_label": "Delivered projects till date",
        "stat2_value": "150,000+",
        "stat2_label": "Happy families",
        "leader_name": "Mohit Goel",
        "leader_designation": "CEO, Omaxe Limited",
        "leader_img_url": "https://randomuser.me/api/portraits/men/1.jpg"
    },
    {
        "name": "VTP REALTY",
        "logo_url": "https://www.vtprealty.com/images/vtp-logo.png",
        "stat1_value": "300+ homes",
        "stat1_label": "Selling Every Month",
        "stat2_value": "35 Lakh+ sqft",
        "stat2_label": "Delivered",
        "leader_name": "Sachin Bhandari",
        "leader_designation": "CEO, VTP Realty",
        "leader_img_url": "https://randomuser.me/api/portraits/men/2.jpg"
    },
    {
        "name": "SPR CITY",
        "logo_url": "https://sprcity.com/wp-content/uploads/2021/04/spr-city-logo.png",
        "stat1_value": "63 acres",
        "stat1_label": "Integrated township",
        "stat2_value": "75+",
        "stat2_label": "Amenities",
        "leader_name": "Navin Ranka",
        "leader_designation": "Director, SPR Group",
        "leader_img_url": "https://randomuser.me/api/portraits/men/3.jpg"
    },
    {
        "name": "HM GROUP",
        "logo_url": "https://hmconstructions.com/assets/images/logo.png",
        "stat1_value": "57+",
        "stat1_label": "Completed projects",
        "stat2_value": "10K+",
        "stat2_label": "Happy Families",
        "leader_name": "Fuzail Siwani",
        "leader_designation": "Director, HM Group",
        "leader_img_url": "https://randomuser.me/api/portraits/men/4.jpg"
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
        }
    )
    
    if created:
        logo_temp = download_image(data["logo_url"])
        if logo_temp:
            builder.logo.save(f"{data['name']}_logo.png", File(logo_temp))
        
        leader_temp = download_image(data["leader_img_url"])
        if leader_temp:
            builder.leader_image.save(f"{data['leader_name']}.jpg", File(leader_temp))
        
        builder.save()
        print(f"Created builder: {builder.name}")
    else:
        print(f"Builder {builder.name} already exists.")

print("Populating builders complete!")
