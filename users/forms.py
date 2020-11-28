"""Django from config for Users."""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from appointment.models import Meeting

# from users.models import Document
from .models import Profile


class DateInput(forms.DateInput):
    input_type = 'datetime-local'


class UserRegisterForm(UserCreationForm):
    """User register form."""

    email = forms.EmailField()

    class Meta:
        """Fields for email attribute."""

        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserCreateMeetForm(forms.ModelForm):
    """User create meeting form."""
    upload = forms.FileField(required=False)

    class Meta:
        model = Meeting
        fields = ['subject', 'description', 'start_time', 'end_time', 'location', 'contact', 'upload']
        widgets = {'start_time': DateInput(), 'end_time': DateInput()}

        
class UserUpdateDetailForm(forms.ModelForm):
    """Update user detail form."""
    email = forms.EmailField()

    class Meta:
        """Fields for change username and email."""

        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    """Update user profile."""
    class Meta:
        """Field for change the image"""
        model = Profile
        fields = ['image', 'university', 'address']

