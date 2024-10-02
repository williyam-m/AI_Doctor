from django.urls import path
from . import views

urlpatterns = [
    path('', views.symptom_checker, name='symptom_checker'),
    path('<int:id>/', views.symptom_detail, name='symptom_detail'),
    path('symptom_history/', views.symptom_history, name='symptom_history')
]
