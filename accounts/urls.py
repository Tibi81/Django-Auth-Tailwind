from django.urls import path
from . import views
from django.urls import path
from django.http import HttpResponse
from .views import home
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('', home, name='home'),  # Gyökérút hozzáadása
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),  # Redirect to 'home' after logout
    path('profile', views.edit_profile, name='profile'),
    path('profile/delete/', views.delete_profile, name='delete_profile'),
]