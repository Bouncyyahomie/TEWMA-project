"""Views for Django appointment app."""
from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Meeting, UserMeeting
from datetime import date, datetime
from datetime import timedelta
from .utils import Calendar
from django.utils.safestring import mark_safe
from django.db.models import Q
from django.contrib import messages
import calendar


def get_date(req_day):
    """Return specific date object if parameter is not the date object, return today otherwise."""
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(month):
    """Return the previous month from current day."""
    first = month.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    """Return the next month from current day."""
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


def meeting_list(request, year, month, day):
    """Render to meeting list of specific day."""
    meetings = Meeting.objects.filter(start_time__year=year, start_time__month=month, start_time__day=day).order_by(
        'start_time')
    context = {'meeting': meetings}
    return render(request, 'appointment/meeting_list.html', context)


def detail(request, meeting_id):
    """Render to meeting's detail page."""
    # meetings = Meeting.objects.get(id=meeting_id)
    meetings = get_object_or_404(Meeting, pk=meeting_id)
    context = {'meeting': meetings}
    return render(request, 'appointment/detail.html', context)


def search(request):
    """Render to meeting list page after search."""
    query = request.GET.get('q')
    if query:
        result = Meeting.objects.filter(Q(subject__icontains=query) | Q(location__icontains=query))
    else:
        result = Meeting.objects.filter()

    context = {'meeting': result}
    return render(request, 'appointment/meeting_list.html', context)


def join(request, meeting_id):
    """For handle when user click join button"""
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    obj, created = UserMeeting.objects.update_or_create(user=request.user, meeting=meeting, defaults={"is_join": True})
    if created:
        messages.success(request, "Successfully Join!!")
    else:
        messages.error(request, "You have joined!!")
    return render(request, 'appointment/detail.html', {'meeting': meeting})
