# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'employment_history', 'education', 'skills']

class LoginForm(AuthenticationForm):
    pass
