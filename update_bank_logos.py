import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from properties.models import BankOffer

# Mapping bank names to their local logo filenames
LOGO_MAP = {
    'State Bank of India': 'bank_logos/state_bank_of_india_logo.png',
    'Bank of Baroda':      'bank_logos/bank_of_baroda_logo.png',
    'Bank of Maharashtra': 'bank_logos/bank_of_maharashtra_logo.png',
}

for bank_name, logo_path in LOGO_MAP.items():
    try:
        offer = BankOffer.objects.get(bank_name=bank_name)
        offer.bank_logo = logo_path
        offer.save()
        print(f"[OK] Updated logo for {bank_name} -> {logo_path}")
    except BankOffer.DoesNotExist:
        # Create it if missing
        offer = BankOffer.objects.create(
            bank_name=bank_name,
            bank_logo=logo_path,
            interest_rate=7.30,
            max_tenure=30,
            disbursement_days=18,
            cash_reward=0,
            is_recommended=(bank_name == 'State Bank of India'),
            order=list(LOGO_MAP.keys()).index(bank_name)
        )
        print(f"[NEW] Created entry for {bank_name} with logo")

print("\nDone! All bank logos updated.")
