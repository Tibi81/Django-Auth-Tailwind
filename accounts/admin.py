from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'location', 'birth_date', 'profile_picture', 'user_email')

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'Email'


