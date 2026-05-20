from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from properties.models import Property
from inquiries.models import Inquiry
from properties.forms import PropertyForm, PropertyImageFormSet, PropertyVideoFormSet

@login_required
def dashboard_home(request):
    user_properties = Property.objects.filter(owner=request.user)
    total_properties = user_properties.count()
    published_properties = user_properties.filter(status='published').count()
    featured_properties = user_properties.filter(featured=True).count()
    total_inquiries = Inquiry.objects.filter(property__owner=request.user).count()
    
    context = {
        'total_properties': total_properties,
        'published_properties': published_properties,
        'featured_properties': featured_properties,
        'total_inquiries': total_inquiries,
        'recent_listings': user_properties.order_by('-created_at')[:5],
        'title': 'Dashboard'
    }
    return render(request, 'dashboard/index.html', context)

@login_required
def my_inquiries(request):
    inquiries = Inquiry.objects.filter(property__owner=request.user)
    return render(request, 'dashboard/my_inquiries.html', {'inquiries': inquiries, 'title': 'My Inquiries'})

@login_required
def my_properties(request):
    properties = Property.objects.filter(owner=request.user)
    return render(request, 'dashboard/my_properties.html', {'properties': properties, 'title': 'My Properties'})

@login_required
def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        # Initialize formsets without instance first to get POST data
        image_formset = PropertyImageFormSet(request.POST, request.FILES, prefix='images')
        video_formset = PropertyVideoFormSet(request.POST, request.FILES, prefix='videos')
        
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.owner = request.user
            property_obj.save()
            form.save_m2m()
            
            # Re-initialize with the saved instance
            image_formset = PropertyImageFormSet(request.POST, request.FILES, instance=property_obj, prefix='images')
            video_formset = PropertyVideoFormSet(request.POST, request.FILES, instance=property_obj, prefix='videos')
            
            if image_formset.is_valid() and video_formset.is_valid():
                image_formset.save()
                video_formset.save()
                messages.success(request, f'Property "{property_obj.title}" added successfully!')
                return redirect('dashboard:home')
            else:
                # If formsets fail, we already saved the property. 
                # This is a bit messy, but at least the property is there.
                messages.warning(request, 'Property saved but some media failed to upload.')
                return redirect('dashboard:home')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = PropertyForm()
        image_formset = PropertyImageFormSet(prefix='images')
        video_formset = PropertyVideoFormSet(prefix='videos')
        
    return render(request, 'dashboard/add_property.html', {
        'form': form,
        'image_formset': image_formset,
        'video_formset': video_formset,
        'title': 'Add Property'
    })

@login_required
def edit_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property_obj)
        image_formset = PropertyImageFormSet(request.POST, request.FILES, instance=property_obj)
        video_formset = PropertyVideoFormSet(request.POST, request.FILES, instance=property_obj)
        
        if form.is_valid() and image_formset.is_valid() and video_formset.is_valid():
            form.save()
            image_formset.save()
            video_formset.save()
            messages.success(request, 'Property updated successfully!')
            return redirect('dashboard:my_properties')
    else:
        form = PropertyForm(instance=property_obj)
        image_formset = PropertyImageFormSet(instance=property_obj)
        video_formset = PropertyVideoFormSet(instance=property_obj)
        
    return render(request, 'dashboard/add_property.html', {
        'form': form,
        'image_formset': image_formset,
        'video_formset': video_formset,
        'title': 'Edit Property'
    })

@login_required
def delete_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, owner=request.user)
    if request.method == 'POST':
        property_obj.delete()
        messages.success(request, 'Property deleted successfully!')
        return redirect('dashboard:my_properties')
    return render(request, 'dashboard/delete_confirm.html', {'property': property_obj})
