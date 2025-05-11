# Bejelentkezés, regisztráció, kijelentkezés

from django.shortcuts import render, redirect
from accounts.models import Profile
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.urls import reverse
from accounts.forms import CustomUserCreationForm
from django.utils.timezone import now, timedelta
from accounts.utils.token_utils import generate_email_token


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Token generálás
            token = generate_email_token()
            profile = Profile.objects.create(user=user, email_token=token)

            # Email megerősítő link
            verification_link = settings.SITE_URL + reverse('verify_email', kwargs={'token': token})
            profile.email_token_expires = now() + timedelta(hours=24)  # Lejárati idő hozzáadása

            # Email küldése
            send_mail(
                subject='Email cím megerősítése',
                message=f'Kedves {user.username},\n\nKérlek kattints az alábbi linkre az email címed megerősítéséhez:\n\n{verification_link}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            # Automatikus bejelentkezés (maradhat, vagy törölheted, ha csak megerősítés után akarsz beengedni)
            # login(request, user)

            messages.success(request, 'Sikeres regisztráció! Kérlek erősítsd meg az e-mail címedet a küldött levélben.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not user.profile.email_verified:
                if user.profile.email_token_expires and user.profile.email_token_expires < now():
                    messages.error(request, 'Az email megerősítő link lejárt. Kérj újat!')
                    return redirect('resend_verification')

                messages.error(request, 'Előbb kérlek erősítsd meg az email címedet, mielőtt belépsz.')                
                return redirect('resend_verification')

            
            

            login(request, user)

            # Ellenőrizzük, van-e függő email token a session-ben
            token = request.session.pop('pending_email_token', None)
            if token:
                return redirect('verify_email', token=token)

            return redirect('profile')
        else:
            messages.error(request, 'Helytelen felhasználónév vagy jelszó')
            return render(request, 'registration/login.html', {'username': username})

    
    return render(request, 'registration/login.html')