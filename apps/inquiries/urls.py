from django.urls import path
from . import views

app_name = 'inquiries'

urlpatterns = [
    path('send/<int:property_id>/', views.send_inquiry, name='send_inquiry'),
    path('leads/', views.lead_dashboard, name='lead_dashboard'),
]
