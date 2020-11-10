"""Django participation tests for appointment app."""
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, date, timedelta
from appointment.models import Meeting
from django.contrib.messages import get_messages
from django.contrib.auth.models import User


def create_meeting(subject, description, location, start_time, contact, end_time):
    """For create meeting object."""
    time = timezone.now() + timedelta(days=start_time)
    time_end = timezone.now() + timedelta(days=end_time)
    return Meeting.objects.create(subject=subject, description=description, location=location,
                                  start_time=time, contact=contact, end_time=time_end)


def create_user(username, email, password):
    """For create the user for test."""
    return User.objects.create_user(username=username, email=email, password=password)


class JoiningTest(TestCase):
    """Test joining button."""

    def setUp(self):
        """Set up for test."""
        self.user1 = create_user("User1", "User1@gmail.com", "isp123456")
        self.meeting1 = create_meeting("Subject1", "Easy", "BKK", -1, "191", 10)
        self.joining_url = reverse('appointment:join', args=(self.meeting1.id,))

    def test_message_with_first_joining(self):
        """If join first time. It should show success message."""
        self.client.post(reverse('login'), {'username': 'User1', 'password': 'isp123456'}, follow=True)
        response = self.client.get(self.joining_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Successfully Join!!")

    def test_message_when_already_join(self):
        """If your already join. It should show error message."""
        self.client.post(reverse('login'), {'username': 'User1', 'password': 'isp123456'}, follow=True)
        self.client.get(self.joining_url)
        response = self.client.get(self.joining_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You have joined!!")


class LeavingTest(TestCase):
    """Test leaving button."""

    def setUp(self):
        """Set up for test."""
        self.user1 = create_user("User1", "User1@gmail.com", "isp123456")
        self.meeting1 = create_meeting("Subject1", "Easy", "BKK", -1, "191", 10)
        self.leaving_url = reverse('appointment:leave', args=(self.meeting1.id,))

    def test_message_with_first_leaving(self):
        """If leaving first time. It should show error message."""
        self.client.post(reverse('login'), {'username': 'User1', 'password': 'isp123456'}, follow=True)
        response = self.client.get(self.leaving_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You haven't attended the appointment yet.")


class JoinAndLeaveTest(TestCase):
    """Test if the user click Join and leave button"""

    def setUp(self):
        """Set up for test."""
        self.user1 = create_user("User1", "User1@gmail.com", "isp123456")
        self.meeting1 = create_meeting("Subject1", "Easy", "BKK", -1, "191", 10)
        self.joining_url = reverse('appointment:join', args=(self.meeting1.id,))
        self.leaving_url = reverse('appointment:leave', args=(self.meeting1.id,))

    def test_message_when_join_and_leave_then_join_again(self):
        """If you join and leave and then join again. It has to show the success message."""
        self.client.post(reverse('login'), {'username': 'User1', 'password': 'isp123456'}, follow=True)
        self.client.get(self.joining_url)
        self.client.get(self.leaving_url)
        response = self.client.get(self.joining_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Successfully Join!!")

    def test_message_when_join_and_leave_then_leave_again(self):
        """If you join and leave and then leave again. It has to show the error message."""
        self.client.post(reverse('login'), {'username': 'User1', 'password': 'isp123456'}, follow=True)
        self.client.get(self.joining_url)
        self.client.get(self.leaving_url)
        response = self.client.get(self.leaving_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You haven't attended the appointment yet.")


class MeetingParticipantTest(TestCase):
    """Test participant page."""

    def setUp(self):
        """Set up for test."""
        self.user1 = create_user("User1", "User1@gmail.com", "isp123456")
        self.meeting1 = create_meeting("Subject1", "Easy", "BKK", -1, "191", 10)
        self.joining_url = reverse('appointment:join', args=(self.meeting1.id,))
        self.leaving_url = reverse('appointment:leave', args=(self.meeting1.id,))
        self.participant_url = reverse('appointment:participants', args=(self.meeting1.id,))

    def test_participant_page_with_one_joining_user(self):
        """If has one joining user in a specific meeting. it should show that user in that meeting"""
        self.client.post(reverse('login'), {'username': 'User1', 'password': 'isp123456'}, follow=True)
        self.client.get(self.joining_url)
        response = self.client.get(self.participant_url)
        self.assertQuerysetEqual(response.context['participants'], ['<UserMeeting: User1 has joined in Subject1>'])
