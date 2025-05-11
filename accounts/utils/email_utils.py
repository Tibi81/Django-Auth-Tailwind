# Email küldés logika

from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.contrib import messages
from accounts.models import Profile
from django.http import Http404
from django.utils import timezone
from django.utils.timezone import now
from .token_utils import generate_email_token

def send_verification_email(user, new_email):
    token  = generate_email_token()

    user.profile.email_token = token
    user.profile.pending_email = new_email  # Itt tároljuk el az új email címet
    user.profile.save()
    print(f"Verification email sent to: {new_email}")  # Debug üzenet

    verification_link = settings.SITE_URL + reverse('verify_email', kwargs={'token': token})

    subject = 'Email cím megerősítése'
    message = f'Szia {user.username}!\n\nKérlek kattints az alábbi linkre az email címed megerősítéséhez:\n{verification_link}'

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])



def verify_email(request, token):
    profile = Profile.objects.filter(email_token=token).first()

    # Ha nem találunk profilt, inkább egy értesítést adunk, nem azonnal dobunk kivételt
    if not profile:
        messages.error(request, 'Érvénytelen vagy lejárt megerősítő link.')
        return redirect('login')

    print(f"Profile found with token: {token}")  # Debug üzenet

    # Ellenőrizzük, hogy a token lejárt-e
    if profile.email_token_expires and profile.email_token_expires < now():
        messages.error(request, 'A megerősítő link lejárt. Kérlek kérj újat.')
        return redirect('resend_verification')

    # Első email megerősítés – bejelentkezés nem szükséges
    if not profile.email_verified:
        profile.email_verified = True
        profile.email_token = None  # Token törlése, nem csak üres string
        profile.save()
        messages.success(request, 'Sikeresen megerősítetted az email címed. Most már be tudsz jelentkezni.')
        return redirect('login')

    # Másodlagos email cím megerősítése
    if request.user.is_authenticated:
        if request.user != profile.user:
            messages.error(request, 'Ez az email megerősítő link nem a Te fiókodhoz tartozik.')
            return redirect('login')

        if profile.pending_email:
            user = profile.user
            user.email = profile.pending_email
            user.save()
            profile.pending_email = None  # Töröljük a pending_email mezőt
            profile.email_token = None  # Token törlése
            profile.save()
            messages.success(request, 'Az email címed sikeresen megváltozott.')
            return redirect('profile')

        messages.info(request, 'Ez az email cím már meg van erősítve.')
        return redirect('profile')

    messages.info(request, 'Ez az email cím már meg van erősítve. Jelentkezz be.')
    return redirect('login')



def resend_verification_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            if user.profile.email_verified:
                messages.info(request, 'Ez az email cím már meg van erősítve.')
                return redirect('login')

            # Új token generálás (opcionális – ha mindig újat akarsz)
            token = generate_email_token()
            user.profile.email_token = token
            user.profile.save()

            verification_link = settings.SITE_URL + reverse('verify_email', kwargs={'token': token})
            send_mail(
                subject='Email cím megerősítése – újraküldés',
                message=f'Szia {user.username},\n\nÚjra elküldjük a megerősítő linket:\n{verification_link}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            messages.success(request, 'A megerősítő link újra elküldve. Nézd meg az emailed.')
            return redirect('login')

        except User.DoesNotExist:
            messages.error(request, 'Ehhez az email címhez nem tartozik regisztrált fiók.')
    
    return render(request, 'registration/resend_verification.html')