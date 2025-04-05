from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Kötelező. Adj meg egy érvényes, egyedi email címet.")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ez az email cím már foglalt.")
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("A két jelszó nem egyezik.")

        if len(password1) < 8:
            raise forms.ValidationError("A jelszónak legalább 8 karakter hosszúnak kell lennie.")
        
        if not re.search(r"\d", password1):
            raise forms.ValidationError("A jelszónak tartalmaznia kell legalább egy számot.")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password1):
            raise forms.ValidationError("A jelszónak tartalmaznia kell legalább egy speciális karaktert.")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    
    