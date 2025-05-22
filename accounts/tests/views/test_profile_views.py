from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import Profile
from django.core import mail
from django.utils import timezone
from datetime import timedelta


class ProfileViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tesztuser', password='titkosjelszo', email='regi@example.com')
        self.profile = Profile.objects.create(user=self.user)
        self.client.login(username='tesztuser', password='titkosjelszo')

    def test_profile_view(self):
        """A profil oldal elérhető bejelentkezett felhasználó számára."""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_edit_profile_get(self):
        """A profil szerkesztés GET kérésre működik."""
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')  # vagy bármilyen HTML elem amit vársz

    def test_edit_profile_post_with_email_change(self):
        """Email megváltoztatása esetén verifikációs emailt küld."""
        response = self.client.post(reverse('edit_profile'), {
            'email': 'uj@example.com',
            'first_name': '',
            'last_name': '',
        })
        self.profile.refresh_from_db()
        self.assertNotEqual(self.profile.email_token, '')  # generált token
        self.assertEqual(self.profile.pending_email, 'uj@example.com')
        self.assertGreater(self.profile.email_token_expires, timezone.now())
        self.assertRedirects(response, reverse('profile'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Email cím megerősítése', mail.outbox[0].subject)

    def test_edit_profile_post_without_email_change(self):
        """Ha az email nem változik, csak mentés történik."""
        response = self.client.post(reverse('edit_profile'), {
            'email': 'regi@example.com',
            'first_name': 'Teszt',
            'last_name': 'User',
        })
        self.assertRedirects(response, reverse('profile'))
        self.profile.refresh_from_db()
        self.assertIsNone(self.user.profile.pending_email, '')  # nem változott
        self.assertEqual(len(mail.outbox), 0)

    def test_delete_profile_post(self):
        """Profil törlése POST kéréssel."""
        response = self.client.post(reverse('delete_profile'))
        self.assertRedirects(response, reverse('home'))
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username='tesztuser')

    def test_delete_profile_get(self):
        """Törlési megerősítő oldal GET-re jelenik meg."""
        response = self.client.get(reverse('delete_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Biztosan törölni akarod a profilodat? Ez a művelet nem vonható vissza.')  # vagy sablonban szereplő szöveg
