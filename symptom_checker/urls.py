from django.urls import path
from . import views

urlpatterns = [
    path('create', views.symptom_checker, name='symptom_checker'),
    path('<int:id>/', views.symptom_report, name='symptom_report'),
    path('', views.symptom_dashboard, name='symptom_dashboard')
]
