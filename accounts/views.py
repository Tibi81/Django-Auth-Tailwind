from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Profile
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from datetime import datetime
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


def home(request):
    return render(request, 'home.html')












