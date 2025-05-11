# Profil megtekintés, szerkesztés, email verifikáció
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.urls import reverse
from accounts.forms import ProfileForm
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from accounts.utils.token_utils import generate_email_token



@login_required
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'profile/profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)

        if form.is_valid():
            new_email = form.cleaned_data.get('email')            

            # Ha az email cím változott
            if new_email != profile.user.email:
                token = generate_email_token()
                profile.email_token = token
                profile.email_token_expires = timezone.now() + timedelta(hours=24)  # Lejárati idő hozzáadása
                profile.pending_email = new_email  # Itt tároljuk el az új email címet
                profile.save()

                # Küldj megerősítő emailt az új címre
                verification_link = settings.SITE_URL + reverse('verify_email', kwargs={'token': token})
                try:
                    send_mail(
                        subject='Email cím megerősítése',
                        message=f'Kedves {request.user.username},\n\nKérlek kattints az alábbi linkre az email címed megerősítéséhez:\n\n{verification_link}',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[new_email],
                        fail_silently=False,
                    )
                except Exception as e:
                    messages.error(request, f'Hiba történt az email küldésekor: {e}')
                    return redirect('edit_profile')
                

                # Értesítés az előző email címre
                try:
                    send_mail(
                        subject='Email cím módosítása',
                        message=f'Kedves {request.user.username},\n\nA regisztrált email címedet megváltoztatták. Ha nem te végezted ezt a módosítást, kérlek vedd fel velünk a kapcsolatot.',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[profile.user.email],
                        fail_silently=False,
                    )
                except Exception as e:
                    messages.error(request, f'Hiba történt az email küldésekor: {e}')
                    return redirect('edit_profile') 
                  
                # Visszairányítunk a bejelentkezési oldalra

                messages.success(request, 'Az email cím módosítását megerősítő linket küldtünk az új email címedre.')
                return redirect('login')  # Visszairányítunk a profil oldalra
            else:
                form.save()
                messages.success(request, 'Profil sikeresen frissítve.')
                return redirect('profile')  # Ha nem történt módosítás
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
        messages.success(request, 'A profilod sikeresen törlésre került.')
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
