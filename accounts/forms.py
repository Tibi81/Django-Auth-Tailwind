from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re
from django.forms.widgets import SelectDateWidget
import datetime
from accounts.utils.token_utils import generate_email_token
import logging

logger = logging.getLogger(__name__)

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

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(label="Keresztnév", required=False)
    last_name = forms.CharField(label="Vezetéknév", required=False)
    email = forms.EmailField(label="Email cím", required=True)

    birth_date = forms.DateField(
        label="Születési dátum",
        required=False,
        initial=datetime.date(2000, 1, 1),  # <- ez állítja be az alapértelmezett dátumot
        widget=SelectDateWidget(
            years=sorted(range(1900, datetime.datetime.now().year + 1), reverse=True)  # Fordított sorrendben jeleníti meg
        )
    )

    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio', 'location', 'phone_number', 'birth_date']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Ha átadjuk a user-t, előre kitöltjük a user mezőket
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.user.pk if self.user else None).exists():
            raise forms.ValidationError("Ez az email cím már más felhasználóhoz tartozik.")
        return email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        # Csak akkor frissítjük az email címet, ha ténylegesen megváltozott
        if user.email != self.cleaned_data['email']:
            profile.pending_email = user.email  # Beállítjuk a pending_email mezőt
            print (f"(forms) pending email cím beállítva: {profile.pending_email}")  # Debug üzenet
            print (f"(forms) email cím: {user.email}")
            profile.email_verified = False  # Visszaállítjuk az email_verified mezőt
            print (f"(forms) email verified: {profile.email_verified}")
            if not profile.email_token:
                profile.email_token = generate_email_token()  # Új token generálása
                print (f"(forms) email token: {profile.email_token}")
            logger.info(f"Email changed to: {profile.pending_email}, pending verification.")  # Debug üzenet

        if commit:
            try:
                user.save()
                profile.save()
            except Exception as e:
                logger.info(f"Hiba történt a mentés során: {e}") # Debug üzenet
                raise forms.ValidationError("Nem sikerült frissíteni a profilt. Próbáld újra később.")

        return profile


    