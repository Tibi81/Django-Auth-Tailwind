# Jelszóval kapcsolatos nézetek
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import logout
from accounts.models import Profile # Ha a Profile model itt van

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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            from accounts.models import Profile
            context['profile'] = Profile.objects.filter(user=self.request.user).first()
        return context