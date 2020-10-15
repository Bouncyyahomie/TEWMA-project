"""Config for Django models."""
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Meeting(models.Model):
    """Django model Object for meeting."""

    # user = models.ForeignKey(User , on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        """Return string representative."""
        return self.subject
