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
            if not user.profile.email_verified:
                print(f"User {username} tried to log in without verifying email.")  # Debug üzenet
                messages.error(request, 'Előbb erősítsd meg az email címedet, mielőtt belépsz!!!!!!!.')                
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



@login_required
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'profile/profile.html', {'profile': profile})





from .forms import ProfileForm
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect

@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)

        if form.is_valid():
            new_email = form.cleaned_data.get('email')
            

            # Ha az email cím változott
            if new_email != profile.user.email:
                token = get_random_string(length=64)
                profile.email_token = token
                profile.pending_email = new_email  # Itt tároljuk el az új email címet
                profile.save()

                # Küldj megerősítő emailt az új címre
                verification_link = settings.SITE_URL + reverse('verify_email', args=[token])
                send_mail(
                    subject='Email cím megerősítése',
                    message=f'Kérlek kattints az alábbi linkre az email címed megerősítéséhez: {verification_link}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[new_email],
                    fail_silently=False,
                )

                # Értesítés az előző email címre
                send_mail(
                    subject='Email cím módosítása',
                    message=f'Kedves {request.user.username},\n\nA regisztrált email címedet megváltoztatták. Ha nem te végezted ezt a módosítást, kérlek vedd fel velünk a kapcsolatot.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[profile.user.email],
                    fail_silently=False,
                )

                messages.success(request, 'Az email cím módosítását megerősítő linket küldtünk az új email címedre.')
                return redirect('login')  # Visszairányítunk a profil oldalra
            else:
                form.save()
                messages.success(request, 'Profil sikeresen frissítve.')
                return redirect('login')  # Ha nem történt módosítás
        else:
            messages.error(request, "Hiba történt a mentés során. Ellenőrizd az űrlapot.")
    else:
        form = ProfileForm(instance=profile, user=request.user)

    return render(request, 'profile/edit_profile.html', {'form': form, 'profile': profile})



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

def send_verification_email(user, new_email):
    token = get_random_string(length=64)
    user.profile.email_token = token
    user.profile.pending_email = new_email  # Itt tároljuk el az új email címet
    user.profile.save()
    print(f"Verification email sent to: {new_email}")  # Debug üzenet

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
        profile = get_object_or_404(Profile, email_token=token)
        print(f"Profile found with token: {token}")  # Debug üzenet

        # Első email megerősítés – bejelentkezés nem szükséges
        if not profile.email_verified:
            profile.email_verified = True
            profile.email_token = ''
            profile.save()
            messages.success(request, 'Sikeresen megerősítetted az email címed. Most már be tudsz jelentkezni.')
            return redirect('login')

        # Másodlagos email cím megerősítése (már létező fiókhoz)
        if request.user.is_authenticated:
            if request.user != profile.user:
                messages.error(request, 'Ez az email megerősítő link nem a Te fiókodhoz tartozik.')
                return redirect('login')

            if profile.pending_email:
                user = profile.user
                user.email = profile.pending_email
                user.save()
                profile.pending_email = ''
                profile.email_token = ''
                profile.save()
                messages.success(request, 'Az email címed sikeresen megváltozott.')
                return redirect('profile')

            messages.info(request, 'Ez az email cím már meg van erősítve.')
            return redirect('profile')

        # Ha már megerősítették, de nincs bejelentkezve
        messages.info(request, 'Ez az email cím már meg van erősítve. Jelentkezz be.')
        return redirect('login')

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
