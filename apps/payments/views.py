import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Payment
from properties.models import Property

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@login_required
def initiate_payment(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id, owner=request.user)
    amount = 50000  # Amount in paise (e.g., 500.00 INR)
    
    order_data = {
        'amount': amount,
        'currency': 'INR',
        'payment_capture': '1'
    }
    
    razorpay_order = razorpay_client.order.create(data=order_data)
    
    payment = Payment.objects.create(
        user=request.user,
        property=property_obj,
        amount=amount/100,
        razorpay_order_id=razorpay_order['id'],
        status='pending'
    )
    
    context = {
        'payment': payment,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'amount': amount,
        'property': property_obj,
        'callback_url': request.build_absolute_uri('/payments/callback/')
    }
    return render(request, 'payments/payment_checkout.html', context)

@csrf_exempt
def payment_callback(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id', '')
        order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        
        try:
            razorpay_client.utility.verify_payment_signature(params_dict)
            payment = Payment.objects.get(razorpay_order_id=order_id)
            payment.razorpay_payment_id = payment_id
            payment.razorpay_signature = signature
            payment.status = 'completed'
            payment.save()
            
            # Update property to featured
            if payment.property:
                payment.property.featured = True
                payment.property.save()
            
            messages.success(request, 'Payment successful! Your property is now featured.')
            return redirect('dashboard:my_properties')
        except:
            messages.error(request, 'Payment verification failed.')
            return redirect('dashboard:my_properties')
    return redirect('dashboard:my_properties')
