"""Config for Django admin."""
from django.contrib import admin
from .models import Meeting

class MeetingAdmin(admin.ModelAdmin):

    fieldset  = [
        (None,  {'fields': ['subject']}),
        ('Infomation', {'fields': ['start_time']})
    ]
    list_display = ('subject','start_time','location','contact')

admin.site.register(Meeting,MeetingAdmin)
