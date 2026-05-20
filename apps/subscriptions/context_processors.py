from .utils import get_active_subscription, get_remaining_limits

def subscription_context(request):
    """Context processor to provide subscription info globally."""
    if request.user.is_authenticated:
        active_sub = get_active_subscription(request.user)
        limits = get_remaining_limits(request.user)
        return {
            'active_subscription': active_sub,
            'user_limits': limits,
        }
    return {}
