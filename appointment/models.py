"""Config for Django models."""
from django.db import models
from django.utils import timezone
import datetime

class Meeting(models.Model):
    """Django model Object for meeting."""

    subject = models.CharField(max_length = 100)
    description = models.CharField(max_length = 500)
    location = models.CharField(max_length = 100)
    start_time = models.DateTimeField('start time')
    contact = models.CharField(max_length = 100)
    end_time = models.DateTimeField('end time')

    def __str__(self):
        """Return string representation for Meeting."""
        return f"{self.subject} : {self.location}"

    def was_published_recently(self):
        """Return true if question is published."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.start_time <= now

    def is_published(self):
        """Return true if start date is before than current date."""
        now = timezone.now()
        return self.start_time <= now
    

