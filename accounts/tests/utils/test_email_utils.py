from django.test import TestCase, override_settings
from django.core import mail
from django.contrib.auth.models import User
from accounts.models import Profile
from django.utils.timezone import now
from datetime import timedelta
from accounts.utils.token_utils import generate_email_token
from accounts.utils.email_utils import send_verification_email, verify_email
from django.urls import reverse
from django.contrib.messages import get_messages
from django.utils import timezone
from django.test import RequestFactory
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponse


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

    
        
    def test_send_email_no_token(self):
        # Ellenőrizzük, hogy a token generálása nélkül is működik-e
        self.profile.email_token = None
        self.profile.save()
        send_verification_email(self.user, "invalid-email")
            


        

    def test_verify_email_token_used_with_pending_email(self):
        self.user = User.objects.create_user(username="testuser2", email="test2@example.com", password="testpassword")
        self.profile = Profile.objects.create(user=self.user, email_verified=True, email_token_used=True, pending_email="pending@example.com")
        token = generate_email_token()
        self.profile.email_token = token
        self.profile.email_token_used = True
        self.profile.pending_email = "pending@example.com"
        self.profile.email_token_expires = now() + timedelta(hours=24)
        self.profile.save()

        # Bejelentkezünk, mert a másodlagos email módosítás csak bejelentkezett userrel működik
        self.client.login(username="testuser2", password="testpassword")

        response = self.client.get(reverse('verify_email', kwargs={'token': token}))

        self.profile.refresh_from_db()
        self.assertTrue(self.profile.email_token_used)  # Token visszaállítva

    def test_verify_email_authenticated_user_email_change(self):
        self.user = User.objects.create_user(username="testuser2", email="test2@example.com", password="testpassword")
        self.profile = Profile.objects.create(user=self.user, email_verified=True, email_token_used=True, pending_email="pending@example.com")
        
        
        # Generáljuk és beállítjuk a tokent + pending_email-t

    def setUp(self):
        # Tesztfelület és tesztfelhasználó létrehozása
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', email='oldemail@example.com', password='testpass123')
        self.profile = Profile.objects.create(
            user=self.user,
            pending_email='newemail@example.com',
            email_token='testtoken',
            email_token_expires=timezone.now() + timedelta(days=1),
            email_token_used=False,
            email_verified=False
        )

    def test_email_change(self):
        # Kérés létrehozása az email megerősítéséhez
        request = self.factory.get('/verify-email/testtoken/')
        request.user = self.user

        # Egyszerű get_response függvény létrehozása
        def get_response(request):
            return HttpResponse()

        # Middleware hozzáadása a kéréshez
        SessionMiddleware(get_response).process_request(request)
        MessageMiddleware(get_response).process_request(request)

        # Az email megerősítő függvény meghívása
        response = verify_email(request, token='testtoken')

        # Profil és felhasználó frissítése az adatbázisból
        self.profile.refresh_from_db()
        self.user.refresh_from_db()

        # Ellenőrzés, hogy az email frissült-e
        self.assertEqual(self.user.email, 'newemail@example.com')

        # Ellenőrzés, hogy a függőben lévő email mező üres-e
        self.assertIsNone(self.profile.pending_email)

        # Ellenőrzés, hogy a token használva lett-e
        self.assertTrue(self.profile.email_token_used)

        # Ellenőrizzük, hogy a változásról küldött értesítő email ment ki
        sent = mail.outbox[0]
        self.assertEqual(sent.subject, 'Email cím módosítása')
        self.assertIn('A regisztrált email címedet megváltoztatták. Az új email címed: newemail@example.com', sent.body)
        self.assertIn('oldemail@example.com', sent.to)  # vagy sent.to == ['oldemail@example.com']




    def test_resend_verification_email_post_valid(self):
        self.profile.email_verified = False
        self.profile.save()

        response = self.client.post(reverse('resend_verification_email'), data={'email': self.user.email})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Email cím megerősítése", mail.outbox[0].subject)

    def test_resend_verification_email_post_already_verified(self):
    
        self.profile.email_verified = True
        self.profile.save()
        response = self.client.post(reverse('resend_verification_email'), data={'email': self.user.email})
        messages_list = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Ez az email cím már meg van erősítve." in str(m) for m in messages_list))

    def test_resend_verification_email_post_no_user(self):
        response = self.client.post(reverse('resend_verification_email'), data={'email': 'nonexistent@example.com'})
        messages_list = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Ehhez az email címhez nem tartozik regisztrált fiók." in str(m) for m in messages_list))