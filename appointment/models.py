"""Config for Django models."""
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Q


class MeetingQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (Q(subject__icontains=query) |
                         Q(description__icontains=query) |
                         Q(location__icontains=query) |
                         Q(contact__icontains=query)
                         )
            qs = qs.filter(or_lookup).distinct()  # distinct() is often necessary with Q lookups
        return qs


class MeetingManager(models.Manager):
    def get_queryset(self):
        return MeetingQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class Meeting(models.Model):
    """Django model Object for meeting."""

    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)

    object = MeetingManager()

    def __str__(self):
        """Return string representative."""
        return self.subject

    def get_html_url(self):
        url = reverse("appointment:detail", args=self.id, )
        return f'<a href="{url}"> {self.title} </a>'
