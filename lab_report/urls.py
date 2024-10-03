from django.urls import path
from . import views

urlpatterns = [
    path('', views.lab_report, name='lab_report'),
]