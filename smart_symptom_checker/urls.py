from django.urls import path
from . import views

urlpatterns = [
    path('smart_symptom_checker/', views.smart_symptom_checker, name='smart_symptom_checker'),
    path('symptom_detail/<int:id>/', views.symptom_detail, name='symptom_detail'),
    path('symptom_history/', views.symptom_history, name='symptom_history')
]
