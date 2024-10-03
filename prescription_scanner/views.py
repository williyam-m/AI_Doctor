from django.shortcuts import render
import google.generativeai as genai
from django.conf import settings
import uuid
import markdown
import os

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel(settings.GEMINI_MODEL)


def prescription_scanner(request):
    ai_response = None

    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']

        unique_filename = f"{uuid.uuid4()}.jpg"
        image_path = os.path.join(settings.BASE_DIR, 'prescription_scanner', 'media', unique_filename)

        with open(image_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)

        uploaded_image = genai.upload_file(image_path)

        prompt_message_path = os.path.join(settings.BASE_DIR, 'prescription_scanner', 'prompt', 'prompt.txt')

        with open(prompt_message_path, 'r', encoding='utf-8') as file:
            prompt = file.read()


        response = model.generate_content([uploaded_image, f"\n\n {prompt}"])

        ai_response = response.text
        ai_response = markdown.markdown(ai_response)

        if os.path.exists(image_path):
            os.remove(image_path)


    return render(request, 'prescription_scanner.html', {'response': ai_response})
