from django.contrib import admin
from .models import SubscriptionPlan, UserSubscription, BuyerPropertyViewHistory, PaymentTransaction

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'price', 'duration_days', 'is_unlimited', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('name',)

@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'plan')
    search_fields = ('user__email',)

@admin.register(BuyerPropertyViewHistory)
class BuyerPropertyViewHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'viewed_at')
    search_fields = ('user__email', 'property__title')

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'user', 'plan', 'amount', 'status', 'created_at')
    list_filter = ('status', 'provider')
    search_fields = ('transaction_id', 'user__email')
