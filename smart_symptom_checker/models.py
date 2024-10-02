from django.db import models
from django.utils import timezone

class SymptomReport(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=200)
    core_symptoms = models.TextField()
    duration_weeks = models.IntegerField()
    severity = models.CharField(max_length=50, choices=[('mild', 'Mild'), ('moderate', 'Moderate'), ('severe', 'Severe')])
    location = models.CharField(max_length=200)
    associated_symptoms = models.CharField(max_length=500, blank=True)
    medical_history = models.CharField(max_length=500, blank=True)
    lifestyle_factors = models.CharField(max_length=500, blank=True)
    recent_exposures = models.CharField(max_length=500, blank=True)
    ai_response = models.TextField(blank=True)
    created_date = models.DateTimeField(default=timezone.now)
