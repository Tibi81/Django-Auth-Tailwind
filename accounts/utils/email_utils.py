# Email küldés logika
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import Profile
from django.utils.timezone import now
from .token_utils import generate_email_token
from datetime import timedelta

def send_verification_email(user, new_email):
    token  = generate_email_token()
    user.profile.email_token = token
    user.profile.email_token_expires = now() + timedelta(hours=24)  # Token érvényességének frissítése
    user.profile.email_token_used = False  # Token használatba vétele
   
    user.profile.pending_email = new_email  # Itt tároljuk el az új email címet
    print (f"Token generálva: {token}")  # Debug üzenet
    print (f"Új email cím: {new_email}")  # Debug üzenet
    
    user.profile.save()
    print(f"Verification email sent to: {new_email}")  # Debug üzenet

    verification_link = settings.SITE_URL + reverse('verify_email', kwargs={'token': token})

    subject = 'Email cím megerősítése'
    message = f'Szia {user.username}!\n\nKérlek kattints az alábbi linkre az email címed megerősítéséhez:\n{verification_link}'

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])



from django.utils.timezone import now
from django.contrib import messages
from django.shortcuts import redirect
from accounts.models import Profile
from django.db import IntegrityError

def verify_email(request, token):
    
    
    profile = Profile.objects.filter(email_token=token).first()    
    # Ha nem találunk profilt, inkább egy értesítést adunk, nem azonnal dobunk kivételt
    if not profile:
        messages.error(request, 'Érvénytelen vagy lejárt megerősítő link.')
        return redirect('login')

    # Ellenőrizzük, hogy a token lejárt-e
    if profile.email_token_expires < now():
        messages.error(request, 'A megerősítő link lejárt. Kérlek kérj újat.')
        return redirect('resend_verification')
    
    
    # Ellenőrizzük, hogy a token már felhasználásra került-e
    if profile.email_token_used:
        if profile.pending_email:  # Ha van függőben lévő email cím, engedjük a módosítást!
            profile.email_token_used = False  # Visszaállítjuk a token használatát
            print(f"Token visszaállítása, ha van függő email: {profile.pending_email}")
        else:
            messages.error(request, 'Ellenőrző: A megerősítő link már felhasználásra került.')
            return redirect('login')

    # Első email megerősítés – bejelentkezés nem szükséges
    if not profile.email_verified:
        try:
            profile.email_verified = True
            profile.email_token = None  # Token törlése
            profile.email_token_used = True  #Token használatba vétele
            profile.save(update_fields=['email_verified', 'email_token', 'email_token_used'])
            
            messages.success(request, 'Sikeresen megerősítetted az email címed. Most már be tudsz jelentkezni.')
        except IntegrityError:
            messages.error(request, 'Első: A megerősítő link már felhasználásra került.')
            print(f"IntegrityError: {profile.email_token_used}")  # Debug üzenet
            return redirect('login')
        return redirect('login')
    print(f"Első email megerősítés: {not profile.email_verified}")  # Debug üzenet

    # Másodlagos email cím megerősítése
    if request.user.is_authenticated:
        if request.user != profile.user:
            messages.error(request, 'Ez az email megerősítő link nem a Te fiókodhoz tartozik.')
            return redirect('login')

        if profile.pending_email:
            old_email = profile.user.email  # Régi email cím mentése
            print(f"Belép az email módosítási szakaszba: {profile.pending_email}")
            user = profile.user
            user.email = profile.pending_email
            print (f"Email cím megváltoztatva: {profile.pending_email}")  # Debug üzenet
            user.save(update_fields=['email'])
            profile.refresh_from_db()  # Biztosítjuk, hogy a változás ténylegesen frissüljön
            profile.pending_email = None  # Töröljük a pending_email mezőt
            profile.email_token = None  # Token törlése
            profile.email_token_used = True  # Token használatba vétele
            profile.save(update_fields=['pending_email', 'email_token', 'email_token_used']) # Profil frissítés
            # Most küldjük ki az értesítést a régi email címre!
        try:
            send_mail(
                subject='Email cím módosítása',
                message=f'Kedves {user.username},\n\nA regisztrált email címedet megváltoztatták. A megadott új email címed: {user.email}\n\n Ha nem te végezted ezt a módosítást, kérlek vedd fel velünk a kapcsolatot.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[old_email],  # Most már a régi emailre küldjük!
                fail_silently=False,
            )
        except Exception as e:
            messages.error(request, f'Hiba történt az értesítés küldésekor: {e}')
            messages.success(request, 'Az email címed sikeresen megváltozott.')
            return redirect('profile')

        messages.info(request, 'Ez az email cím már meg van erősítve. Jelentkezz be.')
        return redirect('login')
        

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