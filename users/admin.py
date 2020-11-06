"""Django admin page config of Users."""
from django.contrib import admin
from .models import Profile

admin.site.register(Profile)
