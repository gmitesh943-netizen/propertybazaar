from django.urls import path
from . import views
from . import admin_views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('properties/', views.my_properties, name='my_properties'),
    path('properties/add/', views.add_property, name='add_property'),
    path('inquiries/', views.my_inquiries, name='my_inquiries'),
    path('properties/edit/<int:pk>/', views.edit_property, name='edit_property'),
    path('properties/delete/<int:pk>/', views.delete_property, name='delete_property'),
    
    # Admin Dashboard
    path('admin/login/', admin_views.admin_login_view, name='admin_login'),
    path('admin/', admin_views.admin_dashboard, name='admin_home'),
    path('admin/users/', admin_views.manage_users, name='admin_users'),
    path('admin/users/<int:pk>/', admin_views.admin_user_detail, name='admin_user_detail'),
    path('admin/subscriptions/', admin_views.manage_subscriptions, name='admin_subscriptions'),
    path('admin/properties/', admin_views.manage_properties, name='admin_properties'),
    path('admin/properties/approve/<int:pk>/', admin_views.approve_property, name='approve_property'),
    path('admin/analytics/', admin_views.admin_analytics, name='admin_analytics'),
]
