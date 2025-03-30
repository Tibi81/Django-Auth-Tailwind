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


def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
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





@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        # Profile adatainak frissítése
        profile.bio = request.POST.get('bio', profile.bio)
        profile.location = request.POST.get('location', profile.location)
        profile.birth_date = request.POST.get('birth_date', profile.birth_date)
        profile.save()

        # Jelszó módosítása
        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        if 'old_password' in request.POST and 'new_password1' in request.POST and 'new_password2' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Ne törlődjön a bejelentkezett felhasználó session-ja
                messages.success(request, 'Password updated successfully')
                return redirect('profile')
            else:
                messages.error(request, 'There was an error updating the password')

    else:
        password_form = PasswordChangeForm(user=request.user)

    return render(request, 'profile/profile.html', {'profile': profile, 'password_form': password_form})


@login_required
def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('home')  # Sikeres törlés után irányítsuk a főoldalra
    return render(request, 'profile/delete_profile.html')  # Külön törlési sablon
