"""Config for Django models."""
from django.db import models
from django.urls import reverse


class Meeting(models.Model):
    """Django model Object for meeting."""

    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)

    def __str__(self):
        """Return subject of meeting."""
        return self.subject

    def date_meeting(self):
        """Return string of start time."""
        return self.start_time.strftime('%d %B %Y')

    @property
    def get_html_url(self):
        """Return HTML of detail page."""
        url = reverse("appointment:detail", args=(self.id,))
        return f'<a href="{url}"> {self.subject}</a>'
