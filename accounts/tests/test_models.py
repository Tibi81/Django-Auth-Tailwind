from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.timezone import now, timedelta
from accounts.models import Profile
import datetime

class ProfileModelTest(TestCase):
    def setUp(self):
        # Létrehozunk egy user-t
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Létrehozunk egy Profile-t ehhez a user-hez
        self.profile = Profile.objects.create(
            user=self.user,
            bio='Test bio',
            location='Test location'
            # Ha vannak kötelező mezők, itt add meg őket
        )

    def test_profile_creation(self):
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.bio, 'Test bio')
        self.assertEqual(self.profile.location, 'Test location')

    def test_profile_str_representation(self):
        Profile.objects.filter(user=self.user).delete()
        profile = Profile.objects.create(user=self.user)
        self.assertEqual(str(profile), 'testuser')

    def test_profile_str(self):
        self.assertEqual(str(self.profile), 'testuser')

    def test_profile_default_values(self):
        Profile.objects.filter(user=self.user).delete()
        profile = Profile.objects.create(user=self.user)
        self.assertFalse(profile.email_verified)
        self.assertFalse(profile.email_token_used)

    def test_default_profile_picture_path(self):
        Profile.objects.filter(user=self.user).delete()
        profile = Profile.objects.create(user=self.user)
        self.assertEqual(profile.profile_picture.name, 'profile_pics/default.jpg')

    def test_email_token_generation(self):
        self.assertIsNotNone(self.profile.email_token)
        self.assertTrue(isinstance(self.profile.email_token, str))
        self.assertEqual(len(self.profile.email_token), 36)

    def test_email_token_expires(self):
        self.assertIsNotNone(self.profile.email_token_expires)
        self.assertTrue(isinstance(self.profile.email_token_expires, datetime.datetime))

    def test_email_token_expires_default(self):
        Profile.objects.filter(user=self.user).delete()
        profile = Profile.objects.create(user=self.user, bio='Test bio', location='Test location')
        self.assertIsNotNone(profile.email_token_expires)
        expected_expiry = now() + timedelta(hours=24)
        actual_expiry = profile.email_token_expires
        self.assertAlmostEqual(actual_expiry, expected_expiry, delta=timedelta(seconds=5))

        

    def test_email_verified_default(self):
        self.assertFalse(self.profile.email_verified)
        self.assertFalse(self.profile.email_token_used)
        self.assertIsNone(self.profile.pending_email)

    def test_profile_can_store_pending_email(self):
        Profile.objects.filter(user=self.user).delete()
        profile = Profile.objects.create(user=self.user, pending_email='test@newemail.com')
        self.assertEqual(profile.pending_email, 'test@newemail.com')

    def test_phone_number(self):
        self.profile.phone_number = '1234567890'
        self.profile.save()
        self.assertEqual(self.profile.phone_number, '1234567890')
        self.profile.phone_number = ''
        self.profile.save()
        self.assertEqual(self.profile.phone_number, '')
