from django.test import TestCase, override_settings
from django.core import mail
from django.contrib.auth.models import User
from accounts.models import Profile
from django.utils.timezone import now
from datetime import timedelta
from accounts.utils.token_utils import generate_email_token
from accounts.utils.email_utils import send_verification_email
from django.urls import reverse

@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class EmailVerificationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpassword")
        self.profile = Profile.objects.create(user=self.user, email_verified=False)
    
    def test_send_verification_email(self):
        new_email = "new_email@example.com"
        send_verification_email(self.user, new_email)
        
        # Ellenőrizzük, hogy a felhasználó profiljában tárolódott-e az új email és a token
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.pending_email, new_email)
        self.assertIsNotNone(self.profile.email_token)
        
        # Ellenőrizzük, hogy e-mailt küldtünk ki
        self.assertEqual(len(mail.outbox), 1)  # Az outbox a Django tesztmailjeinek listája
        self.assertIn("Email cím megerősítése", mail.outbox[0].subject)
        self.assertIn("/verify-email/", mail.outbox[0].body)
        self.assertIn(self.profile.email_token, mail.outbox[0].body)
        

    def test_verify_email_valid_token(self):
        token = generate_email_token()
        self.profile.email_token = token
        self.profile.email_token_expires = now() + timedelta(hours=24)
        self.profile.save()
        
        response = self.client.get(f"/verify-email/{token}/")
        self.profile.refresh_from_db()
        
        self.assertTrue(self.profile.email_verified)
        self.assertIsNone(self.profile.email_token)
        self.assertEqual(response.status_code, 302)  # Átirányítás a bejelentkezéshez

    def test_verify_email_invalid_token(self):
        response = self.client.get("/verify-email/invalid_token/")
        self.assertEqual(response.status_code, 302)  # Átirányítás a bejelentkezéshez


    def test_verify_email_expired_token(self):
        token = generate_email_token()
        self.profile.email_token = token
        self.profile.email_token_expires = now() - timedelta(hours=1)  # Token lejárt
        self.profile.save()

        response = self.client.get(reverse('verify_email', kwargs={'token': token}))

        # Ellenőrizzük, hogy az e-mail továbbra sem megerősített
        self.profile.refresh_from_db()
        self.assertFalse(self.profile.email_verified)
        self.assertIsNotNone(self.profile.email_token)  # A token megmarad, mert lejárt

        # Ellenőrizzük, hogy a felhasználó megfelelő üzenetet kapott
        self.assertEqual(response.status_code, 302)  # Átirányítás egy másik oldalra (például új token kérésére)
