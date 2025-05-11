from django.urls import path
from . import views 
from django.http import HttpResponse
from .views.home import home
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from django.templatetags.static import static
from django.conf import settings
from .utils.email_utils import verify_email, send_verification_email, resend_verification_email
from .views.auth_views import register, user_login
from .views.profile_views import profile, edit_profile, delete_profile
from django.contrib.auth.decorators import login_required   
from .views.profile_views import CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView
from .views.password_views import CustomPasswordChangeView, CustomPasswordChangeDoneView
from django.contrib.auth import views as auth_views




urlpatterns = [
    path('', home, name='home'),  # Gyökérút hozzáadása
    #Authentication URLs
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),  # Redirect to 'home' after logout
    #Profile URLs
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/delete/', delete_profile, name='delete_profile'),
    #Password URLs
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset_form'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    # Email verification URLs
    path('verify-email/<str:token>/', verify_email, name='verify_email'),
    path('send-verification-email/', send_verification_email, name='send_verification_email'),
    path('resend-verification-email/', resend_verification_email, name='resend_verification_email'),
    path('resend-verification/', resend_verification_email, name='resend_verification'),
    
    
]

