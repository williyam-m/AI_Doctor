from django import forms
from .models import SymptomReport

class SymptomReportForm(forms.ModelForm):
    class Meta:
        model = SymptomReport
        fields = [
            'core_symptoms',
            'duration_weeks',
            'severity',
            'location',
            'associated_symptoms',
            'medical_history',
            'lifestyle_factors',
            'recent_exposures'
        ]
        widgets = {
            'core_symptoms': forms.Textarea(attrs={'placeholder': 'Describe your symptoms here...', 'rows': 4}),
            'duration_weeks': forms.NumberInput(attrs={'placeholder': 'Number of weeks'}),
            'severity': forms.Select(choices=[('mild', 'Mild'), ('moderate', 'Moderate'), ('severe', 'Severe')]),
            'location': forms.TextInput(attrs={'placeholder': 'Specific body part'}),
            'associated_symptoms': forms.TextInput(attrs={'placeholder': 'Other related issues'}),
            'medical_history': forms.TextInput(attrs={'placeholder': 'Chronic conditions, allergies, medications'}),
            'lifestyle_factors': forms.TextInput(attrs={'placeholder': 'Diet, exercise, sleep, stress'}),
            'recent_exposures': forms.TextInput(attrs={'placeholder': 'Travel, sick contacts'}),
        }
