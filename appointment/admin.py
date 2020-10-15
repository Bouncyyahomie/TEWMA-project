"""Config for Django admin."""
from django.contrib import admin
from .models import Meeting


admin.site.register(Meeting)
