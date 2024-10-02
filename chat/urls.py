from django.urls import path
from . import views

urlpatterns = [
    path('<int:chat_id>/', views.chat_with_ai_doctor, name='chat_with_ai_doctor'),
    path('', views.chat_with_ai_doctor, name='chat_with_ai_doctor_with_id'),
    path('create_chat/', views.create_chat, name='create_chat'),
]
