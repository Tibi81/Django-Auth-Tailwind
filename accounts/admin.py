from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'location', 'birth_date', 'profile_picture', 'user_email', 'email_verified')
    search_fields = ('user__username', 'user__email', 'location')
    list_filter = ('email_verified', 'birth_date')
    ordering = ('user__username',)

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'Email'


