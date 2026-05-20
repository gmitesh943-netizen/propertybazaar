from django.core.management.base import BaseCommand
from django.utils import timezone
from subscriptions.models import UserSubscription
from notifications.models import Notification
from datetime import timedelta

class Command(BaseCommand):
    help = 'Check for expiring subscriptions and notify users'

    def handle(self, *args, **options):
        now = timezone.now()
        seven_days_later = now + timedelta(days=7)
        
        # 1. Notify 7 days before expiry
        expiring_soon = UserSubscription.objects.filter(
            is_active=True,
            end_date__date=seven_days_later.date()
        )
        for sub in expiring_soon:
            Notification.objects.get_or_create(
                user=sub.user,
                title="Subscription Expiring Soon",
                message=f"Your {sub.plan.name} subscription will expire in 7 days on {sub.end_date.date()}. Renew now to avoid interruption."
            )
            self.stdout.write(f"Notified {sub.user.email} about expiry in 7 days")

        # 2. Notify on expiry
        expired_today = UserSubscription.objects.filter(
            is_active=True,
            end_date__lte=now
        )
        for sub in expired_today:
            sub.is_active = False
            sub.save()
            Notification.objects.create(
                user=sub.user,
                title="Subscription Expired",
                message=f"Your {sub.plan.name} subscription has expired. Your account has been reverted to the free plan."
            )
            self.stdout.write(f"Deactivated and notified {sub.user.email} about expiry")
