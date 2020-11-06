"""Django from config for Users."""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    """User register form."""

    email = forms.EmailField()

    class Meta:
        """Fields for email attribute."""

        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserCreateMeetForm():
    """User create meeting form."""

    pass
