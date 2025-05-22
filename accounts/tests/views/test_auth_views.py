from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.contrib.auth.models import User
from django.utils import timezone
from accounts.models import Profile
from datetime import timedelta

class AuthViewTests(TestCase):

    def create_user_with_profile(self, username, email, password):
        user = User.objects.create_user(username=username, email=email, password=password)
        Profile.objects.create(user=user)
        return user

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')

    def test_valid_registration_sends_email_and_creates_token(self):
        response = self.client.post(self.register_url, {
            'username': 'tesztuser',
            'email': 'teszt@example.com',
            'password1': 'Tesztjelszo123!',
            'password2': 'Tesztjelszo123!'
        })

        self.assertRedirects(response, self.login_url)
        self.assertEqual(User.objects.count(), 1)

        user = User.objects.first()
        profile = user.profile

        self.assertFalse(profile.email_verified)
        self.assertIsNotNone(profile.email_token)

        # Ellenőrizzük, hogy email ment ki
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Email cím megerősítése', mail.outbox[0].subject)
        self.assertIn(profile.email_token, mail.outbox[0].body)



    def test_login_with_verified_email_succeeds(self):
        user = self.create_user_with_profile('tesztuser', 'teszt@example.com', 'Teszt1234')
        user.profile.email_verified = True
        user.profile.save()

        response = self.client.post(self.login_url, {
            'username': 'tesztuser',
            'password': 'Teszt1234'
        })
        self.assertRedirects(response, reverse('profile'))

    def test_login_with_unverified_email_fails(self):
        user = self.create_user_with_profile('tesztuser', 'teszt@example.com', 'Teszt1234')
        user.profile.email_verified = False
        user.profile.save()

        response = self.client.post(self.login_url, {
            'username': 'tesztuser',
            'password': 'Teszt1234'
        })

        self.assertRedirects(response, reverse('resend_verification'))
        

    def test_email_verification_success(self):
        user = self.create_user_with_profile('tesztuser', 'teszt@example.com', 'Teszt1234')
        profile = user.profile
        profile.email_token = '12345'
        profile.email_token_expires = timezone.now() + timedelta(hours=24)
        profile.email_verified = False
        profile.save()

        response = self.client.get(reverse('verify_email', args=['12345']))

        self.assertRedirects(response, reverse('login'))
        user.refresh_from_db()
        self.assertTrue(user.profile.email_verified)
        self.assertTrue(user.profile.email_token_used)

    def test_email_verification_expired_token(self):
        user = self.create_user_with_profile('tesztuser', 'teszt@example.com', 'Teszt1234')
        profile = user.profile
        profile.email_token = 'lejart'
        profile.email_token_expires = timezone.now() - timedelta(hours=1)
        profile.email_verified = False
        profile.save()

        response = self.client.get(reverse('verify_email', args=['lejart']))

        self.assertRedirects(response, reverse('resend_verification'))
        user.refresh_from_db()
        self.assertFalse(user.profile.email_verified)
