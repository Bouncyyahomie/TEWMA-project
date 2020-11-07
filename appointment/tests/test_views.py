"""Views Tests"""
from django.test import TestCase
from django.urls import reverse
from appointment.views import get_date
from django.utils import timezone
from datetime import datetime, date, timedelta
from appointment.models import Meeting


def create_meeting(subject, description, location, start_time, contact, end_time):
    """For create meeting object"""
    time = timezone.now() + timedelta(days=start_time)
    time_end = timezone.now() + timedelta(days=end_time)
    return Meeting.objects.create(subject=subject, description=description, location=location, start_time=time, contact=contact, end_time=time_end)


class IndexViewTest(TestCase):
    """Test for TewMa home page."""

    def test_check_default_home_page(self):
        """If user is not authenticated, show Welcome, AnonymousUser"""
        response = self.client.get(reverse('appointment:home_page'))
        self.assertContains(response, "Welcome, AnonymousUser")

    def test_get_date_with_date_object(self):
        """If argument in get_date() is not date object (str) return a date object with specific date"""
        some_date = get_date("2021-3")
        self.assertEqual(some_date, date(2021, 3, 1))


class MeetingListTest(TestCase):
    """Test for meeting list page"""

    def setUp(self):
        """Set up for test"""
        self.today = datetime.now()
        self.today_day = self.today.day
        self.today_month = self.today.month
        self.today_year = self.today.year
        self.today_url = reverse('appointment:meet_list', args=(self.today.year, self.today.month, self.today.day,))

    def test_no_meeting(self):
        """If no meeting should see noting"""
        response = self.client.get(self.today_url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['meeting'], [])

    def test_with_end_meeting(self):
        """If has end meeting but access in wrong url should see noting"""
        create_meeting("Subject1", "Easy", "BKK", -2, "191", -1)
        response = self.client.get(self.today_url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['meeting'], [])

    def test_with_future_meeting(self):
        """If has future meeting but access in wrong url should see noting"""
        create_meeting("Subject1", "Easy", "BKK", -5, "191", 10)
        response = self.client.get(self.today_url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['meeting'], [])

    def test_with_meeting_in_that_day(self):
        """If access correct url and has meeting on that day should see the detail"""
        create_meeting("Subject1", "Easy", "BKK", 0, "191", 10)
        response = self.client.get(self.today_url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['meeting'], ['<Meeting: Subject1>'])


class MeetingDetailView(TestCase):
    """Test for meeting detail view"""

    def test_can_see_the_detail_of_end_meeting(self):
        """Even after the meeting's closing days, the user still see that meeting"""
        meeting1 = create_meeting("Subject1", "Easy", "BKK", -5, "191", -1)
        meeting_detail_url = reverse('appointment:detail', args=(meeting1.id,))
        response = self.client.get(meeting_detail_url)
        self.assertEqual(response.status_code, 200)

    def test_can_see_the_detail_of_future_meeting(self):
        """User can see future meeting"""
        meeting1 = create_meeting("Subject1", "Easy", "BKK", 5, "191", 10)
        meeting_detail_url = reverse('appointment:detail', args=(meeting1.id,))
        response = self.client.get(meeting_detail_url)
        self.assertEqual(response.status_code, 200)
