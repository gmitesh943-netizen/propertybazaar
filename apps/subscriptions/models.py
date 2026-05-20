from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class SubscriptionPlan(models.Model):
    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('agent', 'Agent'),
    )
    
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField(help_text="Validity in days")
    view_limit = models.PositiveIntegerField(default=0, help_text="Property view limit for buyers (0 if unlimited)")
    post_limit = models.PositiveIntegerField(default=0, help_text="Property post limit for agents (0 if unlimited)")
    is_unlimited = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    features = models.TextField(help_text="Comma separated features", blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_role_display()})"

class UserSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.plan.duration_days)
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return timezone.now() > self.end_date

    def __str__(self):
        return f"{self.user.email} - {self.plan.name}"

class BuyerPropertyViewHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')

class PaymentTransaction(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    provider = models.CharField(max_length=50, help_text="Razorpay, Stripe, etc.")
    transaction_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_id} - {self.status}"
