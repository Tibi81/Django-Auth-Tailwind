from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class PasswordChangeViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tesztuser', password='Teszt1234')
        self.client.login(username='tesztuser', password='Teszt1234')

    def test_password_change_authenticated(self):
        """Ellenőrizzük, hogy a jelszóváltás bejelentkezés után működik-e."""
        response = self.client.get(reverse('password_change'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password/password_change.html')


    def test_password_change_process(self):
        """Ellenőrizzük, hogy a jelszóváltás után átirányítás történik a login oldalra."""
        url = reverse('password_change')
        response = self.client.post(url, {
            'old_password': 'Teszt1234',
            'new_password1': 'newstrongpassword123',
            'new_password2': 'newstrongpassword123',
        }, follow=True)  # Követjük a redirecteket

        # Az utolsó átirányítás után a login oldalon kell lennünk
        self.assertContains(response, "Bejelentkezés")  # vagy amit a login sablon tartalmaz
        self.assertTemplateUsed(response, 'registration/login.html')  # vagy a te login sablonod

        # A felhasználó nincs többé bejelentkezve
        self.assertFalse('_auth_user_id' in self.client.session)


    def test_password_change_done_logs_out_user(self):
    #Ellenőrizzük, hogy sikeres jelszóváltás után a felhasználó ki van léptetve.
    
        # Először váltsunk jelszót
        self.client.post(reverse('password_change'), {
            'old_password': 'Teszt1234',
            'new_password1': 'newstrongpassword123',
            'new_password2': 'newstrongpassword123',
        })

        # Ezután kérjük le a password_change_done oldalt, ami átirányít a login oldalra
        response = self.client.get(reverse('password_change_done'))
        self.assertRedirects(response, reverse('login'))

        # A sessionból eltűnt a bejelentkezett user
        self.assertFalse('_auth_user_id' in self.client.session)

        # Próbáljunk bejelentkezni a régi jelszóval – sikertelenül
        login_failed = self.client.login(username='tesztuser', password='Teszt1234')
        self.assertFalse(login_failed)

        # Próbáljunk bejelentkezni az új jelszóval – sikeresen
        login_success = self.client.login(username='tesztuser', password='newstrongpassword123')
        self.assertTrue(login_success)

