"""Views for Django appointment app."""
from django.shortcuts import render , get_object_or_404, get_list_or_404
from django.views import generic
from .models import Meeting
from datetime import date, datetime
from datetime import timedelta
from .utils import Calendar
from django.utils.safestring import mark_safe
import calendar

def get_date(req_day):
    """Return specific date object if parameter is a date object, return today otherwise."""
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(month):
    first = month.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

class IndexView(generic.ListView):
    """Show a Calendar."""

    model = Meeting
    template_name = 'appointment/home_page.html'

    def get_context_data(self, **kwargs):
        """Return context which is html_calendar."""
        context = super().get_context_data(**kwargs)
        this_day = get_date(self.request.GET.get('month', None))
        calendar = Calendar(this_day.year, this_day.month)
        html_calendar = calendar.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_calendar)
        context['prev_month'] = prev_month(this_day)
        context['next_month'] = next_month(this_day)
        return context

def meeting_list(request, day):
    meetings = Meeting.objects.filter(start_time__day=day)
    context = {'meeting': meetings} 
    return render(request, 'appointment/meeting_list.html', context)

def detail(request,meeting_id):
    # meetings = Meeting.objects.get(id=meeting_id)
    meetings = get_object_or_404(Meeting, pk=meeting_id)
    context = {'meeting': meetings}
    return render(request, 'appointment/detail.html', context)