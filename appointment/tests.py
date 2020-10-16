"""Tests for Django project"""
import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .utils import Calendar
from .models import Meeting

# def create_meeting(subject, description, location, start_time, contact, end_time):
#     time = timezone.now() + datetime.timedelta(days=start_time)
#     time_end = timezone.now() + datetime.timedelta(days=end_time)
#     return Meeting.objects.create(subject = subject , description = description, location = location, start_time = time , contact = contact , end_time = time_end)



class MeetingModelTest(TestCase):
    """Tests for Django Model."""

    # def test_was_published_recently_with_future_meeting(self):
    #     time = timezone.now() + datetime.timedelta(days = 30)
    #     future_meeting = Meeting(start_time = time)
    #     self.assertIs(future_meeting.was_published_recently(), False)


class IndexViewTest(TestCase):
    """Test for TewMa home page."""

    def test_check_home_page(self):
        response = self.client.get(reverse('appointment:home_page'))
        self.assertContains(response, "Welcome, AnonymousUser")
