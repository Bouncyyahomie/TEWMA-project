from django import forms
from .models import Meeting
from django.utils import timezone
from datetime import date
import datetime


class DateInput(forms.DateInput):
    """Datetime picker type."""
    input_type = 'datetime-local'


class UserCreateMeetForm(forms.ModelForm):
    """User create meeting form."""

    class Meta:
        model = Meeting
        fields = ['subject', 'description', 'start_time', 'end_time', 'location', 'contact', 'upload']
        widgets = {'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'min': (datetime.datetime.now() - datetime.timedelta(days=365 * 10)).strftime("%Y-%m-%dT%H:%M"), 'max': (
            datetime.datetime.now() + datetime.timedelta(days=365 * 10)).strftime("%Y-%m-%dT%H:%M"), 'value': datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")}), 'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'min': (datetime.datetime.now() - datetime.timedelta(days=365 * 10)).strftime("%Y-%m-%dT%H:%M"), 'max': (
            datetime.datetime.now() + datetime.timedelta(days=365 * 10)).strftime("%Y-%m-%dT%H:%M"), 'value': (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M")})}


class UserEditMeetForm(forms.ModelForm):
    """User edit meeting form."""

    class Meta:
        model = Meeting
        fields = ['subject', 'description', 'start_time', 'end_time', 'location', 'contact', 'upload']
