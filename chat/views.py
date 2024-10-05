from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import *
import google.generativeai as genai
from django.conf import settings
import markdown
import os

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel(settings.GEMINI_MODEL)



def chat_with_ai_doctor(request, chat_id=None):
    try:
        if request.method == 'POST':
            user_input = request.POST.get('user_input')
            chat_id = request.POST.get('chat_id')

            try:
                chat = Chat.objects.get(id=chat_id)
            except Exception as e:
                return redirect('/chat')

            prompt_message_path = os.path.join(settings.BASE_DIR, 'chat', 'prompt', 'prompt.txt')

            with open(prompt_message_path, 'r', encoding='utf-8') as file:
                prompt = file.read()


            response = model.generate_content(f'{prompt}: {user_input}')
            ai_response = response.text

            chat.messages.append({"user": user_input, "bot": ai_response})
            chat.save()

            return redirect(f'/chat/{chat_id}')

        user_id = request.user.id
        chats = Chat.objects.filter(user_id=user_id).order_by('-created_date')

        chat = None
        if chat_id:
            try:
                chat = Chat.objects.get(id=chat_id)
            except Exception as e:
                return redirect('/chat')


        return render(request, 'chat_with_ai_doctor.html', {'chats': chats, 'chat': chat})

    except Exception as e:
        return render(request, 'error.html')

@login_required(login_url='login')
def create_chat(request):
    try:
        if request.method == 'POST':
            chat_name = request.POST.get('chat_name')
            user_id = request.user.id
            chat = Chat.objects.create(
                user_id=user_id,
                chat_name=chat_name,
                created_date=timezone.now()
            )
            chat.save()
            return redirect(f'/chat/{chat.id}')
        return render(request, 'create_chat.html')

    except Exception as e:
        return render(request, 'error.html')

