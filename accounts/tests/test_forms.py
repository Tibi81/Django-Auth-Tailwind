from django.test import TestCase
from accounts.forms import CustomUserCreationForm, ProfileForm
from django.contrib.auth.models import User
from accounts.models import Profile


class CustomUserCreationFormTest(TestCase):
    def test_valid_registration(self):
        form_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "StrongPass1!",
            "password2": "StrongPass1!"
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_email_duplicate(self):
        User.objects.create_user(username="existinguser", email="existing@example.com", password="Test123!")
        form_data = {
            "username": "newuser",
            "email": "existing@example.com",
            "password1": "StrongPass1!",
            "password2": "StrongPass1!"
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Ez az email cím már foglalt.", form.errors["email"])



class ProfileFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="Test123!")
        self.profile = Profile.objects.create(user=self.user, email_verified=True)

    def test_valid_profile_update(self):
        """Teszteljük, hogy a profil módosítása működik-e érvényes adatokkal"""
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "newemail@example.com",
            "bio": "Ez egy teszt bio.",
            "location": "Budapest",
            "phone_number": "+36301234567",
            "birth_date": "1995-07-15"
        }
        form = ProfileForm(data=form_data, user=self.user, instance=self.profile)
        self.assertTrue(form.is_valid())

    def test_email_change_requires_verification(self):
        """Teszteljük, hogy az email módosítás valóban függő állapotba kerül és új tokent kap"""
        form_data = {
            "email": "changedemail@example.com"
        }
        form = ProfileForm(data=form_data, user=self.user, instance=self.profile)
        self.assertTrue(form.is_valid())

        profile = form.save(commit=False)
        self.assertEqual(profile.pending_email, "test@example.com")  # Régi email függőben
        self.assertFalse(profile.email_verified)  # Email még nem verifikált
        self.assertIsNotNone(profile.email_token)  # Új token generálva

    def test_duplicate_email_error(self):
        """Ellenőrizzük, hogy az email cím duplikáció megfelelően kezelve van"""
        User.objects.create_user(username="existinguser", email="existing@example.com", password="Test123!")
        form_data = {
            "email": "existing@example.com"
        }
        form = ProfileForm(data=form_data, user=self.user, instance=self.profile)
        self.assertFalse(form.is_valid())
        self.assertIn("Ez az email cím már más felhasználóhoz tartozik.", form.errors["email"])

