"""Config for Django admin."""
from django.contrib import admin
from .models import Meeting

class MeetingAdmin(admin.ModelAdmin):
    """Set up page's fields."""

    fieldset = [
        (None, {'fields': ['subject']}),
        ('Infomation', {'fields': ['start_time']})
    ]
    list_display = ('id', 'subject', 'start_time', 'location', 'contact')
    search_field = ['subject']


admin.site.register(Meeting, MeetingAdmin)
