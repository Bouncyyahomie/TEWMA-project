"""Django models tests for appointment app."""
import datetime
from django.test import TestCase
from django.utils import timezone
from appointment.models import Meeting, UserMeeting
from django.contrib.auth.models import User


def create_meeting(subject, description, location, start_time, contact, end_time):
    """For create meeting object."""
    time = timezone.now() + datetime.timedelta(days=start_time)
    time_end = timezone.now() + datetime.timedelta(days=end_time)
    return Meeting.objects.create(subject=subject, description=description, location=location,
                                  start_time=time, contact=contact, end_time=time_end)


def create_user(username, email, password):
    """For create the user for test."""
    return User.objects.create_user(username=username, email=email, password=password)


class MeetingModelTest(TestCase):
    """Tests for Meeting Model."""

    def setUp(self):
        """Set up for test."""
        self.meeting1 = create_meeting("Subject1", "Easy", "BKK", -1, "191", 10)

    def test_str_meeting(self):
        """Test representation of Meeting object."""
        self.assertEqual(str(self.meeting1), "Subject1")

    def test_get_html_url_from_meeting(self):
        """Test if it can get a URL from the Meeting object."""
        self.assertEqual(self.meeting1.get_html_url, '<a href="/1/detail"> Subject1</a>')

    def test_get_meeting_date(self):
        """Test if it can get the meeting date."""
        start_time = timezone.now() + datetime.timedelta(days=-1)
        self.assertEqual(self.meeting1.date_meeting(), start_time.strftime('%d %B %Y'))


class UserMeetingModelTest(TestCase):
    """Tests for UserMeeting Model."""

    def setUp(self):
        self.user1 = create_user("User1", "User1@gmail.com", "isp123456")
        self.meeting1 = create_meeting("Subject1", "Easy", "BKK", -1, "191", 10)

    def test_str_user_meeting_when_is_join_false(self):
        """Test representation of UserMeeting object when is_join false."""
        user_meeting1 = UserMeeting.objects.create(user=self.user1, meeting=self.meeting1, is_join=False)
        self.assertEqual(str(user_meeting1), "User1 has left in Subject1")

    def test_str_user_meeting_when_is_join_true(self):
        """Test representation of UserMeeting object when is_join true."""
        user_meeting1 = UserMeeting.objects.create(user=self.user1, meeting=self.meeting1, is_join=True)
        self.assertEqual(str(user_meeting1), "User1 has joined in Subject1")
