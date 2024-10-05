from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import os
import re
import uuid
from .models import UserProfile

@login_required(login_url='login')
def profile(request):
    try:
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        errors = {}

        if request.method == 'POST':
            gender = request.POST.get('gender')
            age = request.POST.get('age')
            height = request.POST.get('height')
            weight = request.POST.get('weight')

            if not gender:
                errors['gender'] = 'Gender is required.'
            if not age or int(age) < 0 or int(age) > 120:
                errors['age'] = 'Please enter a valid age.'
            if not height or int(height) <= 0 or int(height) > 300:
                errors['height'] = 'Please enter a valid height in cm.'
            if not weight or int(weight) <= 0 or int(weight) > 500:
                errors['weight'] = 'Please enter a valid weight in kg.'

            if not errors:
                user_profile.gender = gender
                user_profile.age = age
                user_profile.height = height
                user_profile.weight = weight
                user_profile.save()
                return redirect('profile')

        return render(request, 'profile.html', {'user_profile': user_profile, 'errors': errors})

    except Exception as e:
        return render(request, 'error.html')


def register(request):
    try:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']

            username_pattern = re.compile(r'^[a-zA-Z0-9._-]+$')
            if not username_pattern.match(username):
                messages.info(request, 'Invalid username!')
                return redirect('/user/register')

            email_pattern = re.compile(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$')
            if not email_pattern.match(email):
                messages.info(request, 'Invalid email address!')
                return redirect('/user/register')

            if password == confirm_password:
                if User.objects.filter(email=email).exists():
                    messages.info(request, 'Email Taken')
                    return redirect('/user/register')
                elif User.objects.filter(username=username).exists():
                    messages.info(request, 'Username Taken')
                    return redirect('/user/register')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()

                    user_login = auth.authenticate(username=username, password=password)
                    auth.login(request, user_login)

                    return redirect('/')
            else:
                messages.info(request, 'Password Not Matching')
                return redirect('/user/register')

        else:
            return render(request, 'register.html')

    except Exception as e:
        return render(request, 'error.html')


def login(request):
    try:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'Credentials Invalid')
                return redirect('/user/login')

        else:
            return render(request, 'login.html')

    except Exception as e:
        return render(request, 'error.html')


@login_required(login_url='login')
def logout(request):
    try:
        auth.logout(request)
        return redirect('/user/login')

    except Exception as e:
        return render(request, 'error.html')