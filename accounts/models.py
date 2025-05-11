from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now, timedelta
import uuid

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    email_token = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    email_token_expires = models.DateTimeField(null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    pending_email = models.EmailField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.email_token_expires:
            self.email_token_expires = now() + timedelta(hours=24)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

