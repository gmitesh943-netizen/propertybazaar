from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('plans/', views.plan_list, name='plan_list'),
    path('subscribe/<int:plan_id>/', views.subscribe, name='subscribe'),
    path('payment/callback/<str:transaction_id>/', views.payment_callback, name='payment_callback'),
    path('status/', views.subscription_status, name='status'),
]
