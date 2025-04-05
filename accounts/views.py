from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Profile
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User


def home(request):
    return render(request, 'home.html')
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})




def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid credentials'})
    return render(request, 'registration/login.html')





from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from datetime import datetime
from .models import Profile  # Importáld a Profile modellt

from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Profile

@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        # Update user fields
        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.last_name = request.POST.get('last_name', request.user.last_name)
        request.user.save()  # Save the user object to persist first_name and last_name changes

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
                return redirect('profile')

        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']

        profile.save()  # Save the profile object to persist changes

        return redirect('profile')  # Redirect to the profile page after successful update


        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        if 'old_password' in request.POST and 'new_password1' in request.POST and 'new_password2' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Jelszó sikeresen frissítve.')
                return redirect('profile')
            else:
                messages.error(request, 'Hiba történt a jelszó frissítése közben.')
    else:
        password_form = PasswordChangeForm(user=request.user)

    return render(request, 'profile/profile.html', {
        'profile': profile,
        'password_form': password_form
    })




@login_required
def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('home')  # Sikeres törlés után irányítsuk a főoldalra
    return render(request, 'profile/delete_profile.html')  # Külön törlési sablon
