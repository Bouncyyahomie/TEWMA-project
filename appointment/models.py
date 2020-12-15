"""Config for Django models."""
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError


class Meeting(models.Model):
    """Django model Object for meeting."""

    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    upload = models.FileField(upload_to='doc/pdfs', blank=True, null=True)
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        """Return subject of meeting."""
        return self.subject

    def date_meeting(self):
        """Return string of start time."""
        return self.start_time.strftime('%d %B %Y')

    def is_ended(self):
        """Is meeting it end now."""
        now = timezone.now()
        return now >= self.end_time

    def clean(self):
        """Override to check if start time is less than or equal to end time."""
        if self.start_time > self.end_time:
            raise ValidationError("Start time should be before end time")
        return super().clean()

    @property
    def get_html_url(self):
        """Return HTML of detail page."""
        url = reverse("appointment:detail", args=(self.id,))
        return f'<a href="{url}"> {self.subject}</a>'

    def get_absolute_url(self):
        return reverse('appointment:detail', kwargs={'meeting_id': self.pk})


class UserMeeting(models.Model):
    """The model for handle users in one meeting."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    is_join = models.BooleanField(default=False)

    def __str__(self):
        """Return user status in specific meeting."""
        if self.is_join:
            return f"{self.user.username} has joined in {self.meeting.subject}"
        return f"{self.user.username} has left in {self.meeting.subject}"
