from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import random
from .forms import UserUpdateForm, ProfileUpdateForm, CustomUserCreationForm
from .models import User

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            
            if settings.DEBUG:
                # Auto-verify in debug mode for easier testing
                user.is_verified = True
                user.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, f'Account created and verified automatically! Welcome, {user.first_name}.')
                return redirect('properties:home')
            
            # Normal OTP flow
            otp = str(random.randint(100000, 999999))
            user.otp = otp
            user.save()
            try:
                send_mail(
                    'Your PropertyBazaar OTP',
                    f'Your OTP is {otp}',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
                messages.info(request, f'OTP has been sent to {user.email}. Please check your email.')
            except Exception as e:
                messages.warning(request, f'Could not send email: {str(e)}. Your OTP is {otp} (shown for debug).')
            
            request.session['verify_user_id'] = user.id
            return redirect('accounts:verify_otp')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def verify_otp(request):
    user_id = request.session.get('verify_user_id')
    if not user_id:
        return redirect('accounts:register')
    
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        user = User.objects.filter(id=user_id).first()
        
        if not user:
            return redirect('accounts:register')
            
        if user.otp == otp_entered or (settings.DEBUG and otp_entered == '000000'):
            user.is_verified = True
            user.otp = None
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Account verified successfully!')
            return redirect('properties:home')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            
    return render(request, 'accounts/verify_otp.html')

def login_view(request):
    if request.method == 'POST':
        identifier = request.POST.get('login_id')
        password = request.POST.get('password')
        
        user = User.objects.filter(email=identifier).first() or User.objects.filter(phone_number=identifier).first()
        
        if user:
            if user.check_password(password):
                if not user.is_verified:
                    if settings.DEBUG:
                        # Auto-verify existing users in debug mode
                        user.is_verified = True
                        user.save()
                    else:
                        # Send new OTP
                        otp = str(random.randint(100000, 999999))
                        user.otp = otp
                        user.save()
                        send_mail(
                            'Your PropertyBazaar OTP',
                            f'Your OTP is {otp}',
                            settings.EMAIL_HOST_USER,
                            [user.email],
                            fail_silently=True,
                        )
                        request.session['verify_user_id'] = user.id
                        messages.info(request, 'Your account was not verified. A new OTP has been sent.')
                        return redirect('accounts:verify_otp')
                
                # Log them in
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, f'Welcome back, {user.first_name}!')
                
                next_url = request.GET.get('next') or request.POST.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('properties:home')
            else:
                messages.error(request, 'Invalid password. Please try again.')
        else:
            messages.error(request, 'No account found with this email or phone number. Please register first.')
            
    return render(request, 'account/login.html')

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('accounts:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'title': 'Profile Settings'
    }
    return render(request, 'accounts/profile.html', context)

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            otp = str(random.randint(100000, 999999))
            user.otp = otp
            user.save()
            send_mail(
                'Password Reset OTP',
                f'Your OTP for resetting password is {otp}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            request.session['reset_user_id'] = user.id
            messages.info(request, f'An OTP has been sent to {email}.')
            return redirect('accounts:verify_reset_otp')
        else:
            messages.error(request, 'No account found with this email.')
    return render(request, 'accounts/forgot_password.html')

def verify_reset_otp(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('accounts:forgot_password')
        
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        user = User.objects.get(id=user_id)
        if user.otp == otp_entered:
            user.otp = None
            user.save()
            request.session['can_reset_password'] = True
            return redirect('accounts:set_new_password')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
    return render(request, 'accounts/verify_reset_otp.html')

def set_new_password(request):
    if not request.session.get('can_reset_password'):
        return redirect('accounts:forgot_password')
        
    user_id = request.session.get('reset_user_id')
    user = User.objects.get(id=user_id)
    
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password == confirm_password:
            user.set_password(password)
            user.save()
            # Clean up session
            del request.session['can_reset_password']
            del request.session['reset_user_id']
            
            messages.success(request, 'Password reset successfully! You can now log in.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Passwords do not match.')
            
    return render(request, 'accounts/set_new_password.html')

@login_required
@csrf_exempt
def ping_time(request):
    if request.method == 'POST':
        profile = request.user.profile
        profile.time_spent_minutes += 1
        profile.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'invalid'})
