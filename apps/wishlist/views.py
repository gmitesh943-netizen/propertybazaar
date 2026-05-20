from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import WishlistItem
from properties.models import Property

@login_required
def wishlist_toggle(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id)
    wishlist_item, created = WishlistItem.objects.get_or_create(user=request.user, property=property_obj)
    
    if not created:
        wishlist_item.delete()
        messages.info(request, 'Property removed from wishlist.')
    else:
        messages.success(request, 'Property added to wishlist.')
        
    return redirect(request.META.get('HTTP_REFERER', 'properties:property_list'))

@login_required
def wishlist_list(request):
    items = WishlistItem.objects.filter(user=request.user)
    return render(request, 'wishlist/wishlist_list.html', {'items': items, 'title': 'My Wishlist'})
