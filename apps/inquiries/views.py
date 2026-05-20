from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from .forms import InquiryForm
from properties.models import Property

from django.http import JsonResponse
from .models import Inquiry

@require_POST
def send_inquiry(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id)
    form = InquiryForm(request.POST)
    
    if form.is_valid():
        inquiry = form.save(commit=False)
        inquiry.property = property_obj
        if request.user.is_authenticated:
            inquiry.user = request.user
        inquiry.save()
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Inquiry sent successfully!'})
            
        messages.success(request, 'Your inquiry has been sent to the property owner.')
        return redirect('properties:property_detail', slug=property_obj.slug)
    else:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
            
        messages.error(request, 'There was an error in your inquiry form.')
        return redirect('properties:property_detail', slug=property_obj.slug)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def lead_dashboard(request):
    if request.user.role not in ['agent', 'builder', 'admin']:
        messages.error(request, "You don't have access to this dashboard.")
        return redirect('dashboard:home')
        
    inquiries = Inquiry.objects.filter(property__owner=request.user).order_by('-created_at')
    return render(request, 'inquiries/lead_dashboard.html', {'inquiries': inquiries})
