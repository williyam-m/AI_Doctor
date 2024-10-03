from django.urls import path
from . import views

urlpatterns = [
    path('', views.prescription_scanner, name='prescription_scanner'),
]