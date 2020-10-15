from django.shortcuts import render
from django.views import generic
from .models import Meeting
from datetime import date, datetime
from .utils import Calendar
from django.utils.safestring import mark_safe

# Create your views here.

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

class IndexView(generic.ListView):
    model = Meeting
    template_name = 'home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        this_day = get_date(self.request.GET.get('month', None))
        calendar = Calendar(this_day.year, this_day.month)
        html_calendar = calendar.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_calendar)
        return context

