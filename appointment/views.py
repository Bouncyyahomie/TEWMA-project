"""Views for Django appointment app."""
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db.models import Q
from django.utils.safestring import mark_safe

from .models import Meeting, UserMeeting
from datetime import date, datetime
from datetime import timedelta
from .utils import Calendar
from django.utils.safestring import mark_safe
from django.db.models import Q
from django.contrib import messages

from django.contrib.auth.decorators import login_required

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
    count = 0
    if query:
        if Meeting.objects.filter(Q(subject__icontains=query) | Q(location__icontains=query)) is not None:
            result = Meeting.objects.filter(Q(subject__icontains=query) | Q(location__icontains=query)).distinct()
            count = result.count()
        else:
            result = None
    else:
        result = None
    context = {'meeting': result, 'query': query, 'count': count}
    return render(request, 'appointment/search_result.html', context)


@login_required
def join(request, meeting_id):
    """For handle when user click join button."""
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    user_meeting = UserMeeting.objects.filter(user=request.user).filter(meeting=meeting).first()
    if user_meeting is None:  # if the user never press the join button before.
        UserMeeting.objects.create(user=request.user, meeting=meeting, is_join=True)
        messages.success(request, "Successfully Join!!")
        return render(request, 'appointment/detail.html', {'meeting': meeting})
    if user_meeting.is_join:  # if the user join the meeting already.
        messages.error(request, "You have joined!!")
        return render(request, 'appointment/detail.html', {'meeting': meeting})
    obj, created = UserMeeting.objects.update_or_create(user=request.user, meeting=meeting, defaults={"is_join": True})
    if obj.is_join:  # if the user press the leave button before.
        messages.success(request, "Successfully Join!!")
    return render(request, 'appointment/detail.html', {'meeting': meeting})


def autocomplete(request):
    if 'term' in request.GET:
        query = Meeting.objects.filter(subject__contains=request.get('term'))
        meets = list()
        for meet in query:
            meets.append(meet.subject)
        return JsonResponse(meets, safe=False)
    return render(request, 'appointment/home_page.html')


@login_required
def leave(request, meeting_id):
    """Leave from the specific appointment."""
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    user_meeting = UserMeeting.objects.filter(user=request.user, meeting=meeting).first()
    if user_meeting is None:  # if the user never press the join button before.
        messages.error(request, "You haven't attended the appointment yet.")
        return render(request, 'appointment/detail.html', {'meeting': meeting})
    if not user_meeting.is_join:  # if the user leave the meeting already.
        messages.error(request, "You haven't attended the appointment yet.")
        return render(request, 'appointment/detail.html', {'meeting': meeting})
    obj, created = UserMeeting.objects.update_or_create(
        user=request.user, meeting=meeting, defaults={"is_join": False})
    if not obj.is_join:  # if the user press the join button before.
        messages.success(request, f"Leaving the appointment, {meeting} is complete.")
    return render(request, 'appointment/detail.html', {'meeting': meeting})


def appointment_participants(request, meeting_id):
    """Show the participant on each appointment."""
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    participants = UserMeeting.objects.filter(meeting=meeting, is_join=True)
    return render(request, 'appointment/participants.html', {'participants': participants})
