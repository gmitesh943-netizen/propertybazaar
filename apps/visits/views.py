from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SiteVisit
from properties.models import Property

@login_required
def schedule_visit(request, property_id):
    if request.method == 'POST':
        property_obj = get_object_or_404(Property, id=property_id)
        visit_date = request.POST.get('visit_date')
        visit_time = request.POST.get('visit_time')
        message = request.POST.get('message', '')
        
        SiteVisit.objects.create(
            user=request.user,
            property=property_obj,
            visit_date=visit_date,
            visit_time=visit_time,
            message=message
        )
        messages.success(request, 'Site visit scheduled successfully. The owner will contact you for confirmation.')
        return redirect('properties:property_detail', slug=property_obj.slug)
    return redirect('properties:property_list')

@login_required
def my_visits(request):
    visits = SiteVisit.objects.filter(user=request.user)
    return render(request, 'visits/my_visits.html', {'visits': visits, 'title': 'My Site Visits'})
