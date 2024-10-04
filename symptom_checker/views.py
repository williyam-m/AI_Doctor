from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import SymptomReport
import google.generativeai as genai
from django.conf import settings
import os

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel(settings.GEMINI_MODEL)

@csrf_exempt
def symptom_checker(request):
    if request.method == 'POST':
        core_symptoms = request.POST['core_symptoms']
        duration_weeks = request.POST['duration_weeks']
        severity = request.POST['severity']
        location = request.POST['location']
        associated_symptoms = request.POST['associated_symptoms']
        medical_history = request.POST['medical_history']
        lifestyle_factors = request.POST['lifestyle_factors']
        recent_exposures = request.POST['recent_exposures']

        prompt_message_path = os.path.join(settings.BASE_DIR, 'symptom_checker', 'prompt', 'prompt.txt')

        with open(prompt_message_path, 'r', encoding='utf-8') as file:
            prompt = file.read()

        prompt = prompt.format(
            core_symptoms = core_symptoms,
            duration_weeks = duration_weeks,
            severity = severity,
            location = location,
            associated_symptoms = associated_symptoms,
            medical_history = medical_history,
            lifestyle_factors = lifestyle_factors,
            recent_exposures = recent_exposures)

        response = model.generate_content(prompt)
        ai_response = response.text

        # save the symptom report and ai response
        symptom_report = SymptomReport(
            user_id=request.user.id,
            core_symptoms=core_symptoms,
            duration_weeks=duration_weeks,
            severity=severity,
            location=location,
            associated_symptoms=associated_symptoms,
            medical_history=medical_history,
            lifestyle_factors=lifestyle_factors,
            recent_exposures=recent_exposures,
            ai_response=ai_response
        )
        symptom_report.save()

        return redirect('symptom_report', id=symptom_report.id)

    return render(request, 'symptom_checker.html')

def symptom_report(request, id):
    symptom_report = get_object_or_404(SymptomReport, id=id)
    return render(request, 'symptom_report.html', {'symptom_report': symptom_report})

def symptom_dashboard(request):
    reports = SymptomReport.objects.filter(user_id=request.user.id).order_by('-created_date')
    return render(request, 'symptom_dashboard.html', {'reports': reports})


