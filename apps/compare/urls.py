from django.urls import path
from . import views

app_name = 'compare'

urlpatterns = [
    path('', views.compare_list, name='list'),
    path('add/<int:property_id>/', views.add_to_compare, name='add'),
    path('remove/<int:property_id>/', views.remove_from_compare, name='remove'),
]
