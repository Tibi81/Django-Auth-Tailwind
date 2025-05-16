from django.shortcuts import render
from accounts.models import Profile  # Ha a Profile model itt van

def home(request):
    profile = None
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()  # Betöltjük a bejelentkezett felhasználó profilját
    return render(request, 'home.html', {'profile': profile})
