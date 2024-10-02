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

        # Create the prompt for the AI
        prompt = (
            f"Core Symptoms: {core_symptoms}\n"
            f"Symptom duration: {duration_weeks} weeks\n"
            f"Symptom severity: {severity}\n"
            f"Symptom location: {location}\n"
            f"Associated symptoms: {associated_symptoms}\n"
            f"Medical history: {medical_history}\n"
            f"Lifestyle factors: {lifestyle_factors}\n"
            f"Recent exposures: {recent_exposures}\n\n"
            "Potential Diagnosis:\n"
            "Likely conditions: A list of possible diseases or conditions based on the given symptoms.\n"
            "Differential diagnosis: If multiple conditions are possible, provide a brief comparison of their symptoms and characteristics.\n"
            "Symptom Explanation:\n"
            "Cause of symptoms: Explain the underlying reasons for the experienced symptoms.\n"
            "Effects of condition: Describe the potential consequences of the condition if left untreated.\n"
            "Treatment and Prevention:\n"
            "Recommended treatment: Suggest appropriate treatments, including medications, lifestyle changes, or over-the-counter remedies.\n"
            "Prevention measures: Offer advice on how to prevent the condition or reduce its severity.\n"
            "When to seek medical attention: Clearly indicate when it's necessary to consult a healthcare professional.\n"
            "Additional Information:\n"
            "Risk factors: Identify factors that increase the likelihood of developing the condition.\n"
            "Prognosis: Provide information about the expected course of the illness.\n"
            "Self-care tips: Offer general health advice to support recovery."
        )

        response = model.generate_content(prompt)
        ai_response = response.text

        # Save the symptom report and AI response
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

        return redirect('symptom_detail', id=symptom_report.id)

    return render(request, 'symptom_form.html')

def symptom_detail(request, id):
    symptom_report = get_object_or_404(SymptomReport, id=id)
    return render(request, 'symptom_detail.html', {'symptom_report': symptom_report})

def symptom_history(request):
    reports = SymptomReport.objects.filter(user_id=request.user.id).order_by('-created_date')
    paginator = Paginator(reports, 10)  # 10 reports per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'symptom_history.html', {'page_obj': page_obj})


