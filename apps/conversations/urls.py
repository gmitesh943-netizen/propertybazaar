from django.urls import path
from . import views

app_name = 'conversations'

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('<int:conversation_id>/', views.chat_detail, name='chat_detail'),
    path('start/<int:property_id>/', views.start_conversation, name='start_conversation'),
]
