from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Chat
import google.generativeai as genai
from django.conf import settings
import os

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel(settings.GEMINI_MODEL)


@login_required(login_url='login')
def chat_with_ai_doctor(request, chat_id=None):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        chat_id = request.POST.get('chat_id')

        chat = get_object_or_404(Chat, id=chat_id)

        # Make a request to the Google Generative AI API
        response = model.generate_content(f'You are an AI doctor. Respond only with doctor-patient related answers: {user_input}')
        ai_response = response.text

        # Update chat messages
        chat.messages.append({"user": user_input, "bot": ai_response})
        chat.save()

        return redirect(f'/chat_with_ai_doctor/{chat_id}')

    user_id = request.user.id
    chats = Chat.objects.filter(user_id=user_id).order_by('-created_date')
    print(chat_id)
    if chat_id :
        chat = Chat.objects.get(id=chat_id)
    else:
        chat = None

    return render(request, 'chat_with_ai_doctor.html', {'chats': chats, 'chat': chat})

@login_required(login_url='login')
def create_chat(request):
    if request.method == 'POST':
        chat_name = request.POST.get('chat_name')
        user_id = request.user.id
        chat = Chat.objects.create(
            user_id=user_id,
            chat_name=chat_name,
            created_date=timezone.now()
        )
        chat.save()
        return redirect(f'/chat_with_ai_doctor/{chat.id}')
    return render(request, 'create_chat.html')

