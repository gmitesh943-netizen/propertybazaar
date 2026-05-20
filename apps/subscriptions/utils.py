from django.utils import timezone
from .models import UserSubscription, BuyerPropertyViewHistory, SubscriptionPlan
from properties.models import Property
from django.db.models import Count
from notifications.models import Notification

def get_active_subscription(user):
    """Returns the current active subscription for a user."""
    if not user.is_authenticated:
        return None
    now = timezone.now()
    return UserSubscription.objects.filter(
        user=user, 
        is_active=True, 
        end_date__gt=now
    ).first()

def can_view_property(user, property_obj):
    """Checks if a buyer can view a specific property."""
    if not user.is_authenticated:
        return False
    
    if user.role != 'buyer':
        return True # Sellers/Agents/Admins have no view limits for now

    if BuyerPropertyViewHistory.objects.filter(user=user, property=property_obj).exists():
        return True

    subscription = get_active_subscription(user)
    
    # If active subscription, check limits
    if subscription:
        if subscription.plan.is_unlimited:
            return True
        # Count unique views
        view_count = BuyerPropertyViewHistory.objects.filter(user=user).count()
        if view_count < subscription.plan.view_limit:
            return True
        return False

    # Free limit check
    free_view_limit = 10
    view_count = BuyerPropertyViewHistory.objects.filter(user=user).count()
    return view_count < free_view_limit

def record_property_view(user, property_obj):
    """Records a unique property view for a buyer and notifies on usage."""
    if not user.is_authenticated or user.role != 'buyer':
        return
    
    _, created = BuyerPropertyViewHistory.objects.get_or_create(user=user, property=property_obj)
    if not created:
        return
    
    # Check usage for notification
    limits = get_remaining_limits(user)
    if limits['total'] != 'Unlimited':
        used = limits['used']
        total = limits['total']
        percentage = (used / total) * 100
        
        if used == total:
            Notification.objects.create(user=user, title="Limit Reached", message="You have reached 100% of your property view limit. Upgrade to continue viewing.")
        elif percentage >= 90 and (used-1)/total*100 < 90:
            Notification.objects.create(user=user, title="Usage Alert", message=f"You have used 90% of your property view limit ({used}/{total}).")
        elif percentage >= 80 and (used-1)/total*100 < 80:
            Notification.objects.create(user=user, title="Usage Alert", message=f"You have used 80% of your property view limit ({used}/{total}).")

def can_post_property(user):
    """Checks if an agent can post a new property."""
    if not user.is_authenticated:
        return False
    
    if user.role != 'agent':
        return True # Buyers can't post anyway, Owners might have different limits? 
                   # Requirements specified Agent limit.

    subscription = get_active_subscription(user)
    post_count = Property.objects.filter(owner=user, status='published').count()
    free_post_limit = 50

    # Usage alerts for agents
    total_limit = subscription.plan.post_limit if subscription and not subscription.plan.is_unlimited else free_post_limit
    if not (subscription and subscription.plan.is_unlimited):
        percentage = (post_count / total_limit) * 100
        if post_count == total_limit:
            Notification.objects.get_or_create(user=user, title="Post Limit Reached", message=f"You have used 100% of your property posting limit ({post_count}/{total_limit}). Upgrade to post more.")
        elif percentage >= 90:
            Notification.objects.get_or_create(user=user, title="Usage Alert", message=f"You have used 90% of your property posting limit ({post_count}/{total_limit}).")
    
    if subscription:
        if subscription.plan.is_unlimited:
            return True
        return post_count < subscription.plan.post_limit

    return post_count < free_post_limit

def get_remaining_limits(user):
    """Returns remaining views/posts for the dashboard."""
    if not user.is_authenticated:
        return {}

    subscription = get_active_subscription(user)
    
    if user.role == 'buyer':
        view_count = BuyerPropertyViewHistory.objects.filter(user=user).count()
        if subscription:
            if subscription.plan.is_unlimited:
                return {'type': 'buyer', 'used': view_count, 'total': 'Unlimited', 'remaining': 'Unlimited'}
            return {'type': 'buyer', 'used': view_count, 'total': subscription.plan.view_limit, 'remaining': subscription.plan.view_limit - view_count}
        return {'type': 'buyer', 'used': view_count, 'total': 10, 'remaining': max(0, 10 - view_count)}

    if user.role == 'agent':
        post_count = Property.objects.filter(owner=user, status='published').count()
        if subscription:
            if subscription.plan.is_unlimited:
                return {'type': 'agent', 'used': post_count, 'total': 'Unlimited', 'remaining': 'Unlimited'}
            return {'type': 'agent', 'used': post_count, 'total': subscription.plan.post_limit, 'remaining': subscription.plan.post_limit - post_count}
        return {'type': 'agent', 'used': post_count, 'total': 50, 'remaining': max(0, 50 - post_count)}

    return {}
