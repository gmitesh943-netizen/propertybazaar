from django.urls import path
from . import views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('profile/', views.profile, name='profile'),
    path('ping/', views.ping_time, name='ping_time'),
    
    # OTP-based Password Reset URLs
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-reset-otp/', views.verify_reset_otp, name='verify_reset_otp'),
    path('set-new-password/', views.set_new_password, name='set_new_password'),
]
