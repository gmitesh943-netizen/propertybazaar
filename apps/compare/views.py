from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from properties.models import Property

def add_to_compare(request, property_id):
    compare_list = request.session.get('compare_list', [])
    if property_id not in compare_list:
        if len(compare_list) < 3:
            compare_list.append(property_id)
            request.session['compare_list'] = compare_list
            messages.success(request, 'Property added to comparison.')
        else:
            messages.warning(request, 'You can compare up to 3 properties.')
    else:
        messages.info(request, 'Property is already in comparison list.')
    
    return redirect(request.META.get('HTTP_REFERER', 'properties:property_list'))

def remove_from_compare(request, property_id):
    compare_list = request.session.get('compare_list', [])
    if property_id in compare_list:
        compare_list.remove(property_id)
        request.session['compare_list'] = compare_list
        messages.info(request, 'Property removed from comparison.')
    return redirect('compare:list')

def compare_list(request):
    compare_ids = request.session.get('compare_list', [])
    properties = Property.objects.filter(id__in=compare_ids)
    return render(request, 'compare/compare_list.html', {'properties': properties, 'title': 'Compare Properties'})
