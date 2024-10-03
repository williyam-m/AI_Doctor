from django.shortcuts import render
import google.generativeai as genai
from django.conf import settings
import os

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel(settings.GEMINI_MODEL)


def lab_report(request):
    response = None
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        image_path = 'static/images/image.jpg'  # Save the image temporarily
        with open(image_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)

        # Upload the image
        uploaded_image = genai.upload_file(image_path)

        # Make a request to the generative AI model

        response = model.generate_content([uploaded_image, "\n\nYou are an AI doctor"])

    return render(request, 'upload.html', {'response': response})
