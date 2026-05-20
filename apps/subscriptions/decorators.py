from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
from .utils import can_view_property, can_post_property, record_property_view
from properties.models import Property

def subscription_required_for_property_view(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # We need the property object to check
        property_id = kwargs.get('pk') or kwargs.get('id')
        slug = kwargs.get('slug')
        
        try:
            if property_id:
                property_obj = Property.objects.get(pk=property_id)
            elif slug:
                property_obj = Property.objects.get(slug=slug)
            else:
                return view_func(request, *args, **kwargs)
        except Property.DoesNotExist:
            return view_func(request, *args, **kwargs)

        if not can_view_property(request.user, property_obj):
            messages.warning(request, "You have reached your free property view limit. Please subscribe to continue.")
            return redirect('subscriptions:plan_list')
        
        # If they can view it, record the view (if it's a buyer)
        record_property_view(request.user, property_obj)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def subscription_required_for_property_post(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not can_post_property(request.user):
            messages.warning(request, "You have reached your free property posting limit. Please upgrade your plan to list more properties.")
            return redirect('subscriptions:plan_list')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
