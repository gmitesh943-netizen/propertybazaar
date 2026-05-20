from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SubscriptionPlan, UserSubscription, PaymentTransaction
from .utils import get_active_subscription, get_remaining_limits
from django.utils import timezone

@login_required
def plan_list(request):
    """Displays available subscription plans based on user role."""
    role = request.user.role
    # If role is 'seller', treat as 'agent' for plans or show 'agent' plans? 
    # Usually real estate sites use 'Agent' for professional sellers.
    # The requirement says role = Agent.
    
    plan_role = 'agent' if role in ['agent', 'seller'] else 'buyer'
    plans = SubscriptionPlan.objects.filter(role=plan_role, is_active=True).order_by('price')
    
    # Process features into lists
    for plan in plans:
        if plan.features:
            plan.feature_list = [f.strip() for f in plan.features.split(',') if f.strip()]
        else:
            plan.feature_list = []

    active_sub = get_active_subscription(request.user)
    
    context = {
        'plans': plans,
        'active_sub': active_sub,
        'role': role,
        'title': 'Subscription Plans'
    }
    return render(request, 'subscriptions/plan_list.html', context)

@login_required
def subscribe(request, plan_id):
    """Initiates a subscription (placeholder for payment gateway)."""
    plan = get_object_or_404(SubscriptionPlan, id=plan_id, is_active=True)
    
    # Check if plan matches user role
    user_role_category = 'agent' if request.user.role in ['agent', 'seller'] else 'buyer'
    if plan.role != user_role_category:
        messages.error(request, "This plan is not available for your account type.")
        return redirect('subscriptions:plan_list')

    if request.method == "POST":
        # Create a pending transaction
        transaction = PaymentTransaction.objects.create(
            user=request.user,
            plan=plan,
            amount=plan.price,
            status='pending',
            provider='Manual',
            transaction_id=f"TXN-{timezone.now().timestamp()}-{request.user.id}"
        )
        # Simulate successful payment and callback
        return redirect('subscriptions:payment_callback', transaction_id=transaction.transaction_id)
    
    return render(request, 'subscriptions/checkout.html', {'plan': plan})

@login_required
def payment_callback(request, transaction_id):
    """Handles successful payment (simulated)."""
    transaction = get_object_or_404(PaymentTransaction, transaction_id=transaction_id, user=request.user)
    
    if transaction.status == 'pending':
        # Mark transaction as completed
        transaction.status = 'completed'
        transaction.save()
        
        # Deactivate previous active subscriptions
        UserSubscription.objects.filter(user=request.user, is_active=True).update(is_active=False)
        
        # Create new subscription
        UserSubscription.objects.create(
            user=request.user,
            plan=transaction.plan,
            start_date=timezone.now(),
            is_active=True
        )
        
        messages.success(request, f"Successfully subscribed to {transaction.plan.name}!")
    
    return redirect('dashboard:home') # Redirect to dashboard

@login_required
def subscription_status(request):
    """View current subscription details."""
    active_sub = get_active_subscription(request.user)
    limits = get_remaining_limits(request.user)
    
    if active_sub:
        active_sub.plan.feature_list = [f.strip() for f in active_sub.plan.features.split(',')]
    
    context = {
        'active_sub': active_sub,
        'limits': limits,
        'title': 'My Subscription'
    }
    return render(request, 'subscriptions/status.html', context)
