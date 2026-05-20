from django.db.models import Count, Q
from .models import Property, PropertyType

def navbar_property_stats(request):
    """
    Context processor to inject dynamic property counts into all templates
    for the mega menu in the navbar.
    """
    # Fetch property types that actually have properties for rent
    property_types = PropertyType.objects.annotate(
        rent_count=Count('properties', filter=Q(properties__listing_type='rent'))
    ).filter(rent_count__gt=0).order_by('-rent_count')[:4]
    
    # Collections
    owner_count = Property.objects.filter(owner__role__in=['seller', 'buyer'], listing_type='rent').count()
    verified_count = Property.objects.filter(owner__is_verified=True, listing_type='rent').count()
    exclusive_count = Property.objects.filter(featured=True, listing_type='rent').count()
    
    # Bachelor Friendly Homes (based on an amenity, if exists, else 0)
    bachelor_count = Property.objects.filter(amenities__name__icontains='Bachelor', listing_type='rent').count()
    
    # Budget Friendly
    under_10k = Property.objects.filter(price__lt=10000, listing_type='rent').count()
    under_15k = Property.objects.filter(price__lt=15000, listing_type='rent').count()
    under_20k = Property.objects.filter(price__lt=20000, listing_type='rent').count()

    return {
        'nav_property_types': property_types,
        'nav_owner_count': owner_count,
        'nav_verified_count': verified_count,
        'nav_exclusive_count': exclusive_count,
        'nav_bachelor_count': bachelor_count,
        'nav_under_10k': under_10k,
        'nav_under_15k': under_15k,
        'nav_under_20k': under_20k,
    }
