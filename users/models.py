"""Django model for Users."""
from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    """User's profile."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='anonymous.png', upload_to='profile_pics')

    def __str__(self):
        """Return username of user."""
        return f'Profile of {self.user.username}'

    def save(self, *args, **kwargs):
        """Override save method for reside the image."""
        super().save(*args, **kwargs)

        image = Image.open(self.image.path)
        if image.height > 300 or image.width > 300:
            image.thumbnail((300,300))
            image.save(self.image.path)
