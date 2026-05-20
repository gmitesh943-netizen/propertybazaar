from django.urls import path
from . import views

app_name = 'visits'

urlpatterns = [
    path('schedule/<int:property_id>/', views.schedule_visit, name='schedule'),
    path('my-visits/', views.my_visits, name='my_visits'),
]
