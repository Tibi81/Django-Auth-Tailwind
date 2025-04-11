from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Profile
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from datetime import datetime
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


def home(request):
    return render(request, 'home.html')

from .forms import CustomUserCreationForm

from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth import logout

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'password/password_change.html'
    success_url = reverse_lazy('password_change_done')  # Ez a jelszóváltás után történő átirányítás helye

from django.contrib.auth.views import PasswordChangeDoneView

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'password_change_done.html'

    def get(self, request, *args, **kwargs):
        # Kiléptetjük a felhasználót
        logout(request)
        messages.success(request, "A jelszavad sikeresen megváltozott. Kérlek jelentkezz be új jelszavaddal.")
        # Átirányítjuk a bejelentkezési oldalra
        return redirect('login')  # Itt a 'login' URL-re irányítunk



from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Token generálás
            token = get_random_string(length=64)
            profile = Profile.objects.create(user=user, email_token=token)

            # Email megerősítő link
            verification_link = settings.SITE_URL + reverse('verify_email', args=[token])

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

    




from django.contrib import messages

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Email megerősítés ellenőrzése
            if not user.profile.email_verified:
                messages.error(request, 'Előbb erősítsd meg az email címedet, mielőtt belépsz.')
                return redirect('resend_verification')

            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'registration/login.html', {'error': 'Helytelen felhasználónév vagy jelszó'})
    
    return render(request, 'registration/login.html')



@login_required
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'profile/profile.html', {'profile': profile})





@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        # Update user fields
        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.last_name = request.POST.get('last_name', request.user.last_name)
        request.user.save()

        # Update profile fields
        profile.bio = request.POST.get('bio', profile.bio)
        profile.location = request.POST.get('location', profile.location)
        profile.phone_number = request.POST.get('phone_number', profile.phone_number)

        new_email = request.POST.get('email')
        if new_email and new_email != request.user.email:
            if User.objects.filter(email=new_email).exclude(pk=request.user.pk).exists():
                messages.error(request, "Ez az email cím már más felhasználóhoz tartozik.")
            else:
                request.user.email = new_email
                request.user.save()

        birth_date = request.POST.get('birth_date', '')
        if birth_date:
            try:
                profile.birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
            except ValueError:
                messages.error(request, "Érvénytelen dátumformátum! Használj ÉÉÉÉ-HH-NN formátumot.")
                return redirect('edit_profile')

        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']

        profile.save()

        return redirect('profile')

    # Ha nem POST, csak GET -> rendereljük az oldalt
    return render(request, 'profile/edit_profile.html', {
        'profile': profile,
        'user': request.user,
    })

    



@login_required
def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('home')  # Sikeres törlés után irányítsuk a főoldalra
    return render(request, 'profile/delete_profile.html')  # Külön törlési sablon

class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'password/password_reset_form.html'  # Az általad létrehozott sablon1

class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'password/password_reset_done.html'  # Az általad létrehozott sablon2

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'password/password_reset_confirm.html'  # Az általad létrehozott sablon3
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'password/password_reset_complete.html'  # Az általad létrehozott sablon4

from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

def send_verification_email(user):
    token = get_random_string(length=64)
    user.profile.email_token = token
    user.profile.save()

    verification_link = settings.SITE_URL + reverse('verify_email', args=[token])

    subject = 'Email cím megerősítése'
    message = f'Szia {user.username}!\n\nKérlek kattints az alábbi linkre az email címed megerősítéséhez:\n{verification_link}'

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Profile
from django.http import Http404

def verify_email(request, token):
    try:
        # A profil lekérése a token alapján
        profile = get_object_or_404(Profile, email_token=token)
        
        # Token validálása
        if profile.email_verified:
            messages.info(request, 'Ez az email cím már megerősítve van.')
            return redirect('login')  # Vagy a kívánt oldal
        
        # Email cím megerősítése
        profile.email_verified = True
        profile.email_token = ''  # A token törlése
        profile.save()

        messages.success(request, 'Email cím sikeresen megerősítve!')
        return redirect('login')  # A felhasználó bejelentkezési oldalra navigálása

    except Profile.DoesNotExist:
        raise Http404("Profil nem található vagy érvénytelen token.")


from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib import messages
from django.conf import settings

def resend_verification_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            if user.profile.email_verified:
                messages.info(request, 'Ez az email cím már meg van erősítve.')
                return redirect('login')

            # Új token generálás (opcionális – ha mindig újat akarsz)
            token = get_random_string(length=64)
            user.profile.email_token = token
            user.profile.save()

            verification_link = settings.SITE_URL + reverse('verify_email', args=[token])
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
