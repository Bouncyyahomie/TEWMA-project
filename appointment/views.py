"""Views for Django appointment app."""
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
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
from .forms import UserCreateMeetForm, UserEditMeetForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.urls import reverse

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
        context['day'] = datetime.today().day
        context['month'] = datetime.today().month
        context['year'] = datetime.today().year
        return context


def meeting_list(request, year, month, day):
    """Render to meeting list of specific day."""
    meetings = Meeting.objects.filter(start_time__year=year, start_time__month=month, start_time__day=day).order_by(
        'start_time')
    is_contain = True
    if len(meetings) == 0 :
        is_contain = False
    day = date(year, month, day)
    context = {'meeting': meetings , "day": day.strftime("%d %b %Y"),
                    "is_contain": is_contain}

    return render(request, 'appointment/meeting_list.html', context)


def detail(request, meeting_id):
    """Render to meeting's detail page."""
    meetings = get_object_or_404(Meeting, pk=meeting_id)
    context = {'meeting': meetings}
    if meetings.is_ended():
        messages.error(request, "This meeting is ended.")
        return redirect('appointment:home_page')
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
    return render(request, 'appointment/participants.html', {'participants': participants, 'meeting': meeting})


class CreateMeeting(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    """For create a meeting"""
    model = Meeting
    form_class = UserCreateMeetForm
    template_name = 'appointment/create_meeting.html'
    success_message = "%(subject)s was created successfully!!"

    def form_valid(self, form):
        """Add host permission to user that create meeting."""
        form.instance.host = self.request.user
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        """Get cleaned date form."""
        return self.success_message % dict(
            cleaned_data,
            subject=self.object.subject,
        )


class EditMeeting(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.UpdateView):
    """For edit a meeting. Only host can do this."""
    model = Meeting
    form_class = UserEditMeetForm
    template_name = 'appointment/edit_meeting.html'
    success_message = "%(subject)s was edited successfully!!"

    def form_valid(self, form):
        """Add host permission to user that create meeting."""
        form.instance.host = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """Test the user to edit meeting. The host can editable only."""
        meeting = self.get_object()
        if self.request.user == meeting.host:
            return True
        return False
    
    def get_success_message(self, cleaned_data):
        """Get cleaned date form."""
        return self.success_message % dict(
            cleaned_data,
            subject=self.object.subject,
        )


class DeleteMeeting(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.DeleteView):
    """For delete a meeting. Only host can do this."""
    model = Meeting
    template_name = 'appointment/delete_meeting.html'
    success_url = '/'
    success_message = "%(subject)s was deleted successfully!!"

    def test_func(self):
        """Test the user to delete meeting. The host can deleteable only."""
        meeting = self.get_object()
        if self.request.user == meeting.host:
            return True
        return False

    def get_success_message(self, cleaned_data):
        """Get cleaned date form."""
        return self.success_message % dict(
            cleaned_data,
            subject=self.object.subject,
        )
    
    def delete(self, request, *args, **kwargs):
        """Override delete method for show the success message."""
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(DeleteMeeting, self).delete(request, *args, **kwargs)

def kick(request, meeting_id, user_id):
    """Remove the user from the meeting"""
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    user = get_object_or_404(User, pk=user_id)
    user_meeting = UserMeeting.objects.filter(user=user).filter(meeting=meeting).first()
    if (request.user == meeting.host):
        if user_meeting is not None:
            if not user_meeting.is_join:
                messages.error(request, "This user doesn't joined yet.")
            else:
                obj, created = UserMeeting.objects.update_or_create(user=user, meeting=meeting, defaults={"is_join": False})
                if not obj.is_join:
                    messages.success(request, f"Kick {user.username} from {meeting.subject} successfully!!")
        else:
            messages.error(request, "This user doesn't joined yet.")
    else:
        messages.error(request, "You don't have that permission!!")
    return redirect('appointment:detail', meeting_id=meeting.id)


@login_required
def subscription(request):
    """Render to subscription page that show what meeting subscribed by a user."""
    # sub_meetings 
    
    return render(request, "appointment/subscription.html")
    