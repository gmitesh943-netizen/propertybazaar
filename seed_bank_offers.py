import os
import django
import sys

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from properties.models import BankOffer
from django.core.files.base import ContentFile
import requests

def seed_bank_offers():
    offers = [
        {
            'name': 'State Bank of India',
            'rate': 7.25,
            'tenure': 30,
            'days': 18,
            'reward': 10000,
            'recommended': True,
            'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/SBI-logo.svg/1200px-SBI-logo.svg.png'
        },
        {
            'name': 'Bank of Maharashtra',
            'rate': 7.10,
            'tenure': 30,
            'days': 18,
            'reward': 20000,
            'recommended': False,
            'logo_url': 'https://upload.wikimedia.org/wikipedia/en/thumb/e/ef/Bank_of_Maharashtra_logo.svg/1200px-Bank_of_Maharashtra_logo.svg.png'
        },
        {
            'name': 'Bank of Baroda',
            'rate': 7.20,
            'tenure': 30,
            'days': 20,
            'reward': 14000,
            'recommended': False,
            'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Bank_of_Baroda_logo.svg/1200px-Bank_of_Baroda_logo.svg.png'
        }
    ]

    for offer_data in offers:
        offer, created = BankOffer.objects.get_or_create(
            bank_name=offer_data['name'],
            defaults={
                'interest_rate': offer_data['rate'],
                'max_tenure': offer_data['tenure'],
                'disbursement_days': offer_data['days'],
                'cash_reward': offer_data['reward'],
                'is_recommended': offer_data['recommended']
            }
        )
        
        # Force update logo if missing
        if not offer.bank_logo:
            try:
                print(f"Downloading logo for {offer_data['name']}...")
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
                response = requests.get(offer_data['logo_url'], headers=headers, timeout=10)
                if response.status_code == 200:
                    file_name = f"{offer_data['name'].lower().replace(' ', '_')}_logo.png"
                    offer.bank_logo.save(file_name, ContentFile(response.content), save=True)
                    print(f"Updated logo for {offer_data['name']}")
                else:
                    print(f"Failed to download logo for {offer_data['name']}: Status {response.status_code}")
            except Exception as e:
                print(f"Error downloading logo for {offer_data['name']}: {e}")
        else:
            print(f"Offer for {offer_data['name']} already has a logo")

if __name__ == "__main__":
    seed_bank_offers()
