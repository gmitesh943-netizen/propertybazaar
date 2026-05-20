import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from subscriptions.models import SubscriptionPlan

def seed_plans():
    plans = [
        # Buyer Plans
        {
            'name': 'Normal Plan',
            'role': 'buyer',
            'price': 499.00,
            'duration_days': 30,
            'view_limit': 100, # Increased from free 10
            'is_unlimited': False,
            'features': 'Priority, Contact, Support'
        },
        {
            'name': 'Paid Plan',
            'role': 'buyer',
            'price': 1299.00,
            'duration_days': 90,
            'view_limit': 0,
            'is_unlimited': True,
            'features': 'Unlimited, Support, Priority'
        },
        {
            'name': 'Premium Plan',
            'role': 'buyer',
            'price': 3999.00,
            'duration_days': 365,
            'view_limit': 0,
            'is_unlimited': True,
            'features': 'Yearly, Unlimited, Dedicated'
        },
        # Agent Plans
        {
            'name': 'Normal Plan',
            'role': 'agent',
            'price': 1999.00,
            'duration_days': 30,
            'post_limit': 200,
            'is_unlimited': False,
            'features': '200_Listings, Analytics, Leads'
        },
        {
            'name': 'Paid Plan',
            'role': 'agent',
            'price': 4999.00,
            'duration_days': 90,
            'post_limit': 500,
            'is_unlimited': False,
            'features': '500_Listings, Featured, Support'
        },
        {
            'name': 'Premium Plan',
            'role': 'agent',
            'price': 14999.00,
            'duration_days': 365,
            'post_limit': 0,
            'is_unlimited': True,
            'features': 'Unlimited, Verified, Manager'
        },
    ]

    for plan_data in plans:
        plan, created = SubscriptionPlan.objects.get_or_create(
            name=plan_data['name'],
            role=plan_data['role'],
            defaults=plan_data
        )
        if created:
            print(f"Created {plan.name} for {plan.role}")
        else:
            print(f"Plan {plan.name} for {plan.role} already exists")

if __name__ == '__main__':
    seed_plans()
