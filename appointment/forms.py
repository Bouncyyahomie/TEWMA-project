from django import forms
from .models import Meeting


class DateInput(forms.DateInput):
    """Datetime picker type."""
    input_type = 'datetime-local'


class UserCreateMeetForm(forms.ModelForm):
    """User create meeting form."""

    class Meta:
        model = Meeting
        fields = ['subject', 'description', 'start_time', 'end_time', 'location', 'contact', 'upload']
        widgets = {'start_time': DateInput(), 'end_time': DateInput()}

class UserEditMeetForm(forms.ModelForm):
    """User edit meeting form."""

    class Meta:
        model = Meeting
        fields = ['subject', 'description', 'start_time', 'end_time', 'location', 'contact', 'upload']