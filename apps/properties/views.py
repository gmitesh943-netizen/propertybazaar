from collections import defaultdict
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, Count
from django.templatetags.static import static
from accounts.models import User
from django.utils.decorators import method_decorator
from subscriptions.decorators import subscription_required_for_property_view, subscription_required_for_property_post
from .models import Property, Category, PropertyType, Amenity, Builder
from .forms import PropertyForm, PropertyImageFormSet, PropertyVideoFormSet

KNOWN_AHMEDABAD_LOCALITIES = [
    'Vaishnodevi-Gota-Zundal',
    'Bopal & South Bopal',
    'Chandkheda',
    'Rest of Ahmedabad',
    'Satellite',
    'Vastrapur',
    'Bodakdev',
    'Ellisbridge',
    'Naroda',
    'Bopal',
    'South Bopal',
    'Gota',
    'Zundal',
    'Navrangpura',
    'Ambawadi',
    'Prahlad Nagar',
    'Thaltej',
    'Maninagar',
    'Science City',
    'SG Highway',
]

def extract_property_locality(property_obj):
    searchable_text = f"{property_obj.title} {property_obj.address} {property_obj.city}".lower()
    for locality in KNOWN_AHMEDABAD_LOCALITIES:
        if locality.lower() in searchable_text:
            return locality

    address_parts = [part.strip() for part in property_obj.address.split(',') if part.strip()]
    if len(address_parts) >= 2:
        candidate = address_parts[-1]
        if candidate.lower() != property_obj.city.lower():
            return candidate

    return property_obj.city

def build_popular_localities(limit=3):
    locality_stats = defaultdict(lambda: {
        'name': '',
        'total_count': 0,
        'sale_count': 0,
        'price_per_sqft': [],
    })

    properties = Property.objects.filter(status='published').select_related('property_type')
    for property_obj in properties:
        locality = extract_property_locality(property_obj)
        stats = locality_stats[locality]
        stats['name'] = locality
        stats['total_count'] += 1
        if property_obj.listing_type == 'sale':
            stats['sale_count'] += 1
        if property_obj.area:
            stats['price_per_sqft'].append(float(property_obj.price) / property_obj.area)

    popular_localities = []
    for stats in locality_stats.values():
        prices = stats['price_per_sqft']
        min_price = int(min(prices)) if prices else 0
        max_price = int(max(prices)) if prices else 0
        count_basis = stats['sale_count'] or stats['total_count']
        rating = min(4.9, 4.0 + (count_basis * 0.08))

        popular_localities.append({
            'name': stats['name'],
            'property_count': count_basis,
            'total_count': stats['total_count'],
            'min_price_per_sqft': min_price,
            'max_price_per_sqft': max_price,
            'rating': f"{rating:.1f}",
            'review_count': max(3, count_basis * 4 + stats['total_count']),
        })

    return sorted(
        popular_localities,
        key=lambda item: (item['property_count'], item['total_count'], item['max_price_per_sqft']),
        reverse=True
    )[:limit]

def home(request):
    featured_properties = Property.objects.filter(featured=True, status='published')[:6]
    recent_properties = Property.objects.filter(status='published').order_by('-created_at')[:6]
    popular_owner_properties = Property.objects.filter(owner__role='owner', status='published')[:6]
    areas = Property.objects.filter(status='published').values_list('city', flat=True).distinct()
    
    # Snapshot counts
    low_budget_flats = Property.objects.filter(price__lte=5000000, property_type__name='Apartment', status='published').count()
    properties_for_sale = Property.objects.filter(listing_type='sale', status='published').count()
    property_agents = User.objects.filter(role='agent').count()
    residential_projects = Property.objects.filter(status='published').count()

    context = {
        'featured_properties': featured_properties,
        'recent_properties': recent_properties,
        'popular_owner_properties': popular_owner_properties,
        'categories': Category.objects.all(),
        'property_types': PropertyType.objects.all(),
        'areas': areas,
        'popular_localities': build_popular_localities(),
        'builders': Builder.objects.all(),
        'stats': {
            'low_budget': low_budget_flats,
            'for_sale': properties_for_sale,
            'agents': property_agents,
            'projects': residential_projects
        }
    }
    return render(request, 'home.html', context)

def new_projects(request):
    queryset = Property.objects.filter(status='published')
    
    # Dynamic Filtering
    search = request.GET.get('search')
    max_price = request.GET.get('max_price')
    bedrooms = request.GET.get('bedrooms')
    completion_status = request.GET.get('status')
    listing_type = request.GET.get('listing_type')
    
    # Hotspot / Radius Filtering (5 km)
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    active_location = request.GET.get('location', '')
    
    if search:
        queryset = queryset.filter(Q(title__icontains=search) | Q(city__icontains=search))
    if max_price:
        queryset = queryset.filter(price__lte=max_price)
    if bedrooms:
        queryset = queryset.filter(bedrooms=bedrooms)
    if completion_status:
        queryset = queryset.filter(status=completion_status)
    if listing_type:
        queryset = queryset.filter(listing_type=listing_type)

    if lat and lng:
        try:
            from geopy.distance import geodesic
            center = (float(lat), float(lng))
            props_with_coords = queryset.filter(latitude__isnull=False, longitude__isnull=False)
            matching_ids = [
                p.id for p in props_with_coords
                if geodesic(center, (float(p.latitude), float(p.longitude))).km <= 5
            ]
            queryset = queryset.filter(id__in=matching_ids)
        except Exception:
            pass
        
    context = {
        'properties': queryset,
        'title': 'New Projects Encyclopedia',
        'property_types': PropertyType.objects.all(),
        'categories': Category.objects.all(),
        'total_count': queryset.count(),
        'active_location': active_location,
    }
    return render(request, 'projects/new_projects.html', context)

def top_agents(request):
    # Filter users with role 'agent' and count their properties
    agents = User.objects.filter(role='agent').annotate(
        property_count=Count('properties')
    ).order_by('-property_count')
    
    total_agents = User.objects.filter(role='agent').count()
    
    context = {
        'agents': agents,
        'total_agents': total_agents,
        'title': 'Top Real Estate Agents'
    }
    return render(request, 'projects/top_agents.html', context)

def agent_detail(request, pk):
    agent = get_object_or_404(User, pk=pk, role='agent')
    properties = Property.objects.filter(owner=agent, status='published')
    
    context = {
        'agent': agent,
        'properties': properties,
        'title': f'Agent Profile - {agent.get_full_name}'
    }
    return render(request, 'projects/agent_detail.html', context)

def encyclopedia_properties(request):
    queryset = Property.objects.filter(status='published')
    
    # Dynamic Filtering
    search = request.GET.get('search')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    bedrooms = request.GET.get('bedrooms')
    category_id = request.GET.get('category')
    type_id = request.GET.get('type')
    featured = request.GET.get('featured')
    owner_role = request.GET.get('owner_role')
    
    if search:
        queryset = queryset.filter(
            Q(title__icontains=search) | 
            Q(city__icontains=search) |
            Q(property_type__name__icontains=search) |
            Q(category__name__icontains=search)
        )
    if min_price:
        queryset = queryset.filter(price__gte=min_price)
    if max_price:
        queryset = queryset.filter(price__lte=max_price)
    if bedrooms:
        queryset = queryset.filter(bedrooms=bedrooms)
    if category_id:
        queryset = queryset.filter(category_id=category_id)
    if type_id:
        queryset = queryset.filter(property_type_id=type_id)
    if featured:
        queryset = queryset.filter(featured=True)
    if owner_role:
        queryset = queryset.filter(owner__role=owner_role)
        
    context = {
        'properties': queryset,
        'title': 'Properties Encyclopedia',
        'property_types': PropertyType.objects.all(),
        'categories': Category.objects.all(),
        'total_count': queryset.count()
    }
    return render(request, 'projects/encyclopedia_properties.html', context)

class PropertyListView(ListView):
    model = Property
    template_name = 'properties/property_list.html'
    context_object_name = 'properties'
    paginate_by = 9

    def get_queryset(self):
        queryset = Property.objects.filter(status='published')
        
        # Filtering
        city = (self.request.GET.get('city') or '').strip()
        property_type = (self.request.GET.get('type') or '').strip()
        category = (self.request.GET.get('category') or '').strip()
        min_price = (self.request.GET.get('min_price') or '').strip()
        max_price = (self.request.GET.get('max_price') or '').strip()
        bedrooms = (self.request.GET.get('bedrooms') or '').strip()
        
        listing_type = (self.request.GET.get('listing_type') or '').strip()
        lat = (self.request.GET.get('lat') or '').strip()
        lng = (self.request.GET.get('lng') or '').strip()
        
        furnishing = (self.request.GET.get('furnishing') or '').strip()
        possession = (self.request.GET.get('possession') or '').strip()
        posted_by = (self.request.GET.get('posted_by') or '').strip()
        rera = (self.request.GET.get('rera') or '').lower()
        verified = (self.request.GET.get('verified') or '').lower()
        featured = (self.request.GET.get('featured') or '').lower()
        
        has_coordinates = bool(lat and lng)

        if city and not has_coordinates:
            queryset = queryset.filter(
                Q(city__icontains=city) |
                Q(address__icontains=city) |
                Q(state__icontains=city)
            )
        if property_type:
            queryset = queryset.filter(property_type__slug=property_type)
        if category:
            queryset = queryset.filter(category__slug=category)
        if min_price:
            try:
                queryset = queryset.filter(price__gte=min_price)
            except ValueError:
                pass
        if max_price:
            try:
                queryset = queryset.filter(price__lte=max_price)
            except ValueError:
                pass
        if bedrooms:
            try:
                queryset = queryset.filter(bedrooms__gte=int(bedrooms))
            except ValueError:
                pass
        if listing_type in dict(Property.LISTING_TYPE_CHOICES):
            queryset = queryset.filter(listing_type=listing_type)
        if furnishing:
            queryset = queryset.filter(furnishing_status=furnishing)
        if possession:
            queryset = queryset.filter(possession_status=possession)
        if posted_by:
            queryset = queryset.filter(posted_by=posted_by)
        if rera in ['on', 'true', '1', 'yes']:
            queryset = queryset.filter(rera_approved=True)
        if verified in ['on', 'true', '1', 'yes']:
            queryset = queryset.filter(verified=True)
        if featured in ['on', 'true', '1', 'yes']:
            queryset = queryset.filter(featured=True)

        # Radius Search (15 km)
        if has_coordinates:
            try:
                from geopy.distance import geodesic
                center_point = (float(lat), float(lng))
                props_with_coords = queryset.filter(latitude__isnull=False, longitude__isnull=False)
                matching_ids = []
                for prop in props_with_coords:
                    prop_point = (float(prop.latitude), float(prop.longitude))
                    if geodesic(center_point, prop_point).km <= 15:
                        matching_ids.append(prop.id)
                queryset = queryset.filter(id__in=matching_ids)
            except (TypeError, ValueError):
                pass
            
        # Sorting
        sort = self.request.GET.get('sort')
        if sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        else:
            queryset = queryset.order_by('-created_at') # default newest
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['property_types'] = PropertyType.objects.all()
        extracted_locations = {
            extract_property_locality(property_obj)
            for property_obj in Property.objects.filter(status='published').only('title', 'address', 'city')
        }
        context['location_options'] = sorted(set(KNOWN_AHMEDABAD_LOCALITIES) | extracted_locations)
        query_params = self.request.GET.copy()
        query_params.pop('page', None)
        context['filter_querystring'] = query_params.urlencode()
        return context

@method_decorator(subscription_required_for_property_view, name='dispatch')
class PropertyDetailView(DetailView):
    model = Property
    template_name = 'properties/property_detail.html'
    context_object_name = 'property'

    def get_object(self):
        obj = super().get_object()
        obj.views_count += 1
        obj.save()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['similar_properties'] = Property.objects.filter(
            category=self.object.category, 
            status='published'
        ).exclude(id=self.object.id)[:3]
        return context

def propworth(request):
    total_properties = Property.objects.filter(status='published').count()
    handpicked_projects = Property.objects.filter(featured=True, status='published')[:4]
    owner_properties = Property.objects.filter(owner__role='owner', status='published')[:4]
    
    context = {
        'title': 'PropWorth - Estimate Property Value',
        'total_properties': total_properties,
        'handpicked_projects': handpicked_projects,
        'owner_properties': owner_properties,
    }
    return render(request, 'tools/propworth.html', context)

def rates_trends(request):
    return render(request, 'tools/rates_trends.html', {'title': 'Rates & Trends - Market Analysis'})

def buy_vs_rent(request):
    return render(request, 'tools/buy_vs_rent.html', {'title': 'Buy vs Rent - Comparison Tool'})

def tips_guides(request):
    return render(request, 'tools/tips_guides.html', {'title': 'Tips & Guides - Real Estate Advice'})

def interiors_estimator(request):
    return render(request, 'tools/interiors_estimator.html', {'title': 'Interiors Budget Estimator - PropertyBazaar'})

def emi_calculator(request):
    from .models import BankOffer
    bank_offers = BankOffer.objects.all()
    context = {
        'title': 'Home Loan EMI Calculator',
        'bank_offers': bank_offers
    }
    return render(request, 'tools/emi_calculator.html', context)

def stamp_duty(request):
    return render(request, 'tools/stamp_duty.html', {'title': 'Stamp Duty & Registration Calculator'})

def loan_eligibility(request):
    return render(request, 'tools/eligibility.html', {'title': 'Home Loan Eligibility Calculator'})

import random
from django.utils import timezone

def sync_bank_rates():
    """
    Simulates fetching live interest rates from a Bank API/Server.
    In a real-world scenario, this would use requests.get() to an external API.
    """
    from .models import BankOffer
    banks = BankOffer.objects.all()
    
    # Simulating a small change in rates to show it's "Live"
    for bank in banks:
        # Randomly fluctuate rates by +/- 0.05%
        change = random.choice([-0.05, 0, 0.05])
        new_rate = float(bank.interest_rate) + change
        # Keep it within reasonable bounds
        bank.interest_rate = max(6.5, min(9.5, new_rate))
        bank.save()

def bank_offers_detail(request):
    from .models import BankOffer
    
    # Call the sync function to simulate "Online Server Update"
    sync_bank_rates()
    
    bank_offers = BankOffer.objects.all()
    context = {
        'title': 'Compare Home Loan Interest Rates - PropertyBazaar',
        'bank_offers': bank_offers,
        'stats': {
            'customers': '8,100+',
            'cities': '18+',
            'disbursed': '5,000 Crore+'
        },
        'sync_time': timezone.now()
    }
    return render(request, 'tools/bank_offers_detail.html', context)

def loan_application(request):
    if request.method == 'POST':
        city = (request.POST.get('city') or '').strip()
        property_type = request.POST.get('property_type')
        property_status = request.POST.get('property_status')
        property_value = request.POST.get('property_value')

        if city:
            request.session['loan_app_city'] = city
            request.session['loan_app_property_type'] = property_type
            request.session['loan_app_property_status'] = property_status
            request.session['loan_app_property_value'] = property_value
        else:
            request.session.pop('loan_app_city', None)
        return redirect('properties:loan_application_employment')

    popular_cities = [
        {'name': 'Hyderabad', 'image': static('img/cities/city-placeholder.svg')},
        {'name': 'New Delhi', 'image': static('img/cities/city-placeholder.svg')},
        {'name': 'Ahmedabad', 'image': static('img/cities/city-placeholder.svg')},
        {'name': 'Gurgaon', 'image': static('img/cities/city-placeholder.svg')},
        {'name': 'Bangalore', 'image': static('img/cities/city-placeholder.svg')},
        {'name': 'Mumbai', 'image': static('img/cities/city-placeholder.svg')},
        {'name': 'Navi Mumbai', 'image': static('img/cities/city-placeholder.svg')},
        {'name': 'Pune', 'image': static('img/cities/city-placeholder.svg')},
        {'name': 'Thane', 'image': static('img/cities/city-placeholder.svg')},
        {'name': 'Chennai', 'image': static('img/cities/city-placeholder.svg')},
    ]
    context = {
        'title': 'Apply for Home Loan - PropertyBazaar',
        'popular_cities': popular_cities,
        'step': 'property',
        'selected_city': request.session.get('loan_app_city', 'Ahmedabad'),
        'property_type': request.session.get('loan_app_property_type', ''),
        'property_status': request.session.get('loan_app_property_status', ''),
        'property_value': request.session.get('loan_app_property_value', ''),
    }
    return render(request, 'tools/loan_application.html', context)


def loan_application_employment(request):
    if request.method == 'POST':
        employment_type = (request.POST.get('employment_type') or '').strip()
        monthly_income = (request.POST.get('monthly_income') or '').strip()
        company_name = (request.POST.get('company_name') or '').strip()

        request.session['loan_app_employment_type'] = employment_type
        request.session['loan_app_monthly_income'] = monthly_income
        request.session['loan_app_company_name'] = company_name
        return redirect('properties:loan_application_loan')

    context = {
        'title': 'Employment Details - PropertyBazaar',
        'step': 'employment',
        'city': request.session.get('loan_app_city', ''),
        'employment_type': request.session.get('loan_app_employment_type', ''),
        'monthly_income': request.session.get('loan_app_monthly_income', ''),
        'company_name': request.session.get('loan_app_company_name', ''),
    }
    return render(request, 'tools/loan_application_employment.html', context)


def loan_application_loan(request):
    if request.method == 'POST':
        loan_amount = (request.POST.get('loan_amount') or '').strip()
        tenure_years = (request.POST.get('tenure_years') or '').strip()
        purpose = (request.POST.get('purpose') or '').strip()

        request.session['loan_app_loan_amount'] = loan_amount
        request.session['loan_app_tenure_years'] = tenure_years
        request.session['loan_app_purpose'] = purpose
        return redirect('properties:loan_application_profile')

    context = {
        'title': 'Loan Details - PropertyBazaar',
        'step': 'loan',
        'city': request.session.get('loan_app_city', ''),
        'employment_type': request.session.get('loan_app_employment_type', ''),
        'monthly_income': request.session.get('loan_app_monthly_income', ''),
        'loan_amount': request.session.get('loan_app_loan_amount', ''),
        'tenure_years': request.session.get('loan_app_tenure_years', '20'),
        'purpose': request.session.get('loan_app_purpose', 'home-loan'),
    }
    return render(request, 'tools/loan_application_loan.html', context)


def loan_application_profile(request):
    if request.method == 'POST':
        full_name = (request.POST.get('full_name') or '').strip()
        phone = (request.POST.get('phone') or '').strip()
        email = (request.POST.get('email') or '').strip()

        request.session['loan_app_full_name'] = full_name
        request.session['loan_app_phone'] = phone
        request.session['loan_app_email'] = email
        request.session['loan_app_submitted'] = True

    context = {
        'title': 'Profile - PropertyBazaar',
        'step': 'profile',
        'submitted': bool(request.session.get('loan_app_submitted')),
        'data': {
            'city': request.session.get('loan_app_city', ''),
            'property_type': request.session.get('loan_app_property_type', ''),
            'property_status': request.session.get('loan_app_property_status', ''),
            'property_value': request.session.get('loan_app_property_value', ''),
            'employment_type': request.session.get('loan_app_employment_type', ''),
            'monthly_income': request.session.get('loan_app_monthly_income', ''),
            'company_name': request.session.get('loan_app_company_name', ''),
            'loan_amount': request.session.get('loan_app_loan_amount', ''),
            'tenure_years': request.session.get('loan_app_tenure_years', ''),
            'purpose': request.session.get('loan_app_purpose', ''),
            'full_name': request.session.get('loan_app_full_name', ''),
            'phone': request.session.get('loan_app_phone', ''),
            'email': request.session.get('loan_app_email', ''),
        }
    }
    return render(request, 'tools/loan_application_profile.html', context)



from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
@subscription_required_for_property_post
def sell_property(request):
    """Render a form for users to list a new property for sale.
    Restricted to Agents and Builders only."""
    if request.user.role not in ['agent', 'builder']:
        messages.error(request, "Only Agents and Builders can list properties.")
        return redirect('properties:home')
        
    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            prop = form.save(commit=False)
            prop.owner = request.user
            prop.status = "published"
            prop.save()
            # Save many-to-many relationships
            form.save_m2m()
            messages.success(request, "Your property has been listed successfully!")
            return redirect('properties:property_detail', slug=prop.slug)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PropertyForm()
    return render(request, "properties/sell_property.html", {"title": "Sell Property", "form": form})

def home_interiors(request):
    return render(request, 'properties/home_interiors.html', {
        'title': 'Home Interior Design Services - PropertyBazaar',
        'hide_footer_cta': True,
        'hide_navbar': True
    })

def area_converter(request):
    return render(request, 'tools/area_converter.html', {'title': 'Area Converter - PropertyBazaar'})
