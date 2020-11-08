"""Django model for Users."""
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """User's profile."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='anonymous.png', upload_to='profile_pics')

    def __str__(self):
        """Return username of user."""
        return f'Profile of {self.user.username}'
