"""Django from config for Users."""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from appointment.models import Meeting

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
    class Meta:
        model = Meeting
        fields = ['subject', 'description', 'start_time', 'end_time', 'location', 'contact']
        widgets = {'start_time': DateInput(), 'end_time': DateInput()}
