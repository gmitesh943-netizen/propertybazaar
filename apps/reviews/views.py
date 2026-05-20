from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from properties.models import Property

@login_required
def add_review(request, property_id):
    if request.method == 'POST':
        property_obj = get_object_or_404(Property, id=property_id)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        Review.objects.update_or_create(
            user=request.user,
            property=property_obj,
            defaults={'rating': rating, 'comment': comment}
        )
        messages.success(request, 'Your review has been submitted.')
    return redirect('properties:property_detail', slug=property_obj.slug)
