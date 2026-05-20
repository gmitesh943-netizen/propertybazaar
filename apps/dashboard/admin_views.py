from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib import messages
from accounts.models import User
from properties.models import Property
from inquiries.models import Inquiry
from payments.models import Payment # Assuming this exists
from subscriptions.models import UserSubscription
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def admin_dashboard(request):
    total_users = User.objects.count()
    total_properties = Property.objects.count()
    pending_approvals = Property.objects.filter(status='draft').count()
    total_inquiries = Inquiry.objects.count()
    
    total_buyers = User.objects.filter(role='buyer').count()
    total_agents = User.objects.filter(role='agent').count()
    total_sellers = User.objects.filter(role='seller').count()
    
    active_subscribers = UserSubscription.objects.filter(is_active=True, end_date__gte=timezone.now()).values('user').distinct().count()
    
    # Revenue stats (placeholder if Payment model exists)
    try:
        from payments.models import Payment
        total_revenue = Payment.objects.filter(status='completed').aggregate(Sum('amount'))['amount__sum'] or 0
    except:
        total_revenue = 0

    recent_properties = Property.objects.order_by('-created_at')[:5]
    recent_users = User.objects.order_by('-date_joined')[:5]

    context = {
        'total_users': total_users,
        'total_properties': total_properties,
        'pending_approvals': pending_approvals,
        'total_inquiries': total_inquiries,
        'total_buyers': total_buyers,
        'total_agents': total_agents,
        'total_sellers': total_sellers,
        'active_subscribers': active_subscribers,
        'total_revenue': total_revenue,
        'recent_properties': recent_properties,
        'recent_users': recent_users,
    }
    return render(request, 'dashboard/admin/index.html', context)

@user_passes_test(is_admin)
def manage_users(request):
    role = request.GET.get('role')
    users = User.objects.all().order_by('-date_joined')
    if role:
        users = users.filter(role=role)
        if role in ['agent', 'builder']:
            users = users.annotate(
                deals_closed=Count('properties', filter=Q(properties__status__in=['sold', 'rented']))
            )
    return render(request, 'dashboard/admin/users.html', {'users': users, 'current_role': role})

@user_passes_test(is_admin)
def admin_user_detail(request, pk):
    from django.shortcuts import get_object_or_404
    user_obj = get_object_or_404(User, pk=pk)
    subscriptions = UserSubscription.objects.filter(user=user_obj).order_by('-start_date')
    
    stats = {}
    if user_obj.role == 'buyer':
        stats['Time Spent'] = f"{user_obj.profile.time_spent_minutes} minutes"
    elif user_obj.role in ['agent', 'builder']:
        deals = user_obj.properties.filter(status__in=['sold', 'rented']).count()
        stats['Deals Closed'] = deals

    context = {
        'user_obj': user_obj,
        'subscriptions': subscriptions,
        'stats': stats,
    }
    return render(request, 'dashboard/admin/user_detail.html', context)

@user_passes_test(is_admin)
def manage_properties(request):
    properties = Property.objects.all().order_by('-created_at')
    return render(request, 'dashboard/admin/properties.html', {'properties': properties})

@user_passes_test(is_admin)
def manage_subscriptions(request):
    subscriptions = UserSubscription.objects.filter(is_active=True, end_date__gte=timezone.now()).select_related('user', 'plan').order_by('-start_date')
    return render(request, 'dashboard/admin/subscriptions.html', {'subscriptions': subscriptions})

@user_passes_test(is_admin)
def approve_property(request, pk):
    property_obj = Property.objects.get(pk=pk)
    property_obj.status = 'published'
    property_obj.save()
    return redirect('dashboard:admin_properties')

@user_passes_test(is_admin)
def admin_analytics(request):
    # Total Leads
    total_leads = Inquiry.objects.count()
    
    # Active Agents (Most inquiries received)
    active_agents = User.objects.filter(role='agent').annotate(inquiry_count=Count('properties__inquiries')).order_by('-inquiry_count')[:5]
    
    # High Demand Localities
    popular_localities = Property.objects.values('city').annotate(inquiry_count=Count('inquiries')).order_by('-inquiry_count')[:5]
    
    context = {
        'total_leads': total_leads,
        'active_agents': active_agents,
        'popular_localities': popular_localities,
    }
    return render(request, 'dashboard/admin/analytics.html', context)

def admin_login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            messages.success(request, 'Welcome to Admin Dashboard')
            return redirect('dashboard:admin_home')
        else:
            messages.error(request, 'Invalid credentials or you are not an Admin.')
            
    return render(request, 'dashboard/admin/login.html')
