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


class KickTest(TestCase):
    """Test kick button."""

    def setUp(self):
        """Set up for test."""
        self.user1 = create_user("User1", "User1@gmail.com", "isp123456")
        self.host_user = create_user("Host", "Host@gmail.com", "isp123456")
        self.time_start1 = timezone.now()
        self.time_end1 = timezone.now() + timedelta(days=30)

    def test_try_to_kick_a_user_by_host_account(self):
        """Host user has permission for kick a user."""
        #Logged in host user.
        self.client.login(username='Host', password='isp123456')
        #Create meeting with host user.
        self.client.post(reverse('appointment:create-meeting'), {'subject': 'Econ',
                                                                 'description': 'Economic for better living', 'start_time': self.time_start1,
                                                                 'end_time': self.time_end1, 'location': 'KU', 'contact': '191'})
        meeting1 = Meeting.objects.filter(host=self.host_user).first()
        self.client.logout() #Host user has logged out.
        #Logged in User1.
        self.client.login(username='User1', password='isp123456')
        self.joining_url = reverse('appointment:join', args=(meeting1.id,))
        #User1 join meeting1.
        response = self.client.get(self.joining_url)
        self.client.logout() #User1 user has logged out.
        #Logged in Host.
        self.client.login(username='Host', password='isp123456')
        #Before kick
        response = self.client.get(reverse('appointment:participants', args=(meeting1.id,)))
        self.assertQuerysetEqual(response.context['participants'], ['<UserMeeting: User1 has joined in Econ>'])
        response = self.client.get(reverse('appointment:kick', kwargs={'meeting_id': meeting1.id, 'user_id': self.user1.id}))
        messages = list(get_messages(response.wsgi_request))
        #Test message
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f"Kick {self.user1.username} from {meeting1.subject} successfully!!")
        #After kick
        response = self.client.get(reverse('appointment:participants', args=(meeting1.id,)))
        self.assertQuerysetEqual(response.context['participants'], [])

    def test_try_to_kick_a_user_with_the_user_not_have_permission(self):
        """The user not have permission to kick, that user can not kick anyone."""
        #Logged in host user.
        self.client.login(username='Host', password='isp123456')
        #Create meeting with host user.
        self.client.post(reverse('appointment:create-meeting'), {'subject': 'Econ',
                                                                 'description': 'Economic for better living', 'start_time': self.time_start1,
                                                                 'end_time': self.time_end1, 'location': 'KU', 'contact': '191'})
        meeting1 = Meeting.objects.filter(host=self.host_user).first()
        #Host join meeting.
        self.joining_url = reverse('appointment:join', args=(meeting1.id,))
        response = self.client.get(self.joining_url)
        self.client.logout() #Host user has logged out.
        #Logged in User1.
        self.client.login(username='User1', password='isp123456')
        #Before kick
        response = self.client.get(reverse('appointment:participants', args=(meeting1.id,)))
        self.assertQuerysetEqual(response.context['participants'], ['<UserMeeting: Host has joined in Econ>'])
        #Kick host user
        response = self.client.get(reverse('appointment:kick', kwargs={'meeting_id': meeting1.id, 'user_id': self.host_user.id}))
        messages = list(get_messages(response.wsgi_request))
        #Test message
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f"You don't have that permission!!")
        #After kick
        response = self.client.get(reverse('appointment:participants', args=(meeting1.id,)))
        self.assertQuerysetEqual(response.context['participants'], ['<UserMeeting: Host has joined in Econ>'])

    def test_try_to_kick_the_user_does_not_join_yet(self):
        """Can not kick the user that does not join yet."""
        #Logged in host user.
        self.client.login(username='Host', password='isp123456')
        #Create meeting with host user.
        self.client.post(reverse('appointment:create-meeting'), {'subject': 'Econ',
                                                                 'description': 'Economic for better living', 'start_time': self.time_start1,
                                                                 'end_time': self.time_end1, 'location': 'KU', 'contact': '191'})
        meeting1 = Meeting.objects.filter(host=self.host_user).first()
        #Before kick
        response = self.client.get(reverse('appointment:participants', args=(meeting1.id,)))
        self.assertQuerysetEqual(response.context['participants'], [])
        response = self.client.get(reverse('appointment:kick', kwargs={'meeting_id': meeting1.id, 'user_id': self.user1.id}))
        messages = list(get_messages(response.wsgi_request))
        #Test message
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "This user doesn't joined yet.")
        #After kick
        response = self.client.get(reverse('appointment:participants', args=(meeting1.id,)))
        self.assertQuerysetEqual(response.context['participants'], [])

    def test_try_to_kick_the_user_used_to_joined_but_leave_for_now(self):
        """Can not kick the user that leave from meeting."""
        #Logged in host user.
        self.client.login(username='Host', password='isp123456')
        #Create meeting with host user.
        self.client.post(reverse('appointment:create-meeting'), {'subject': 'Econ',
                                                                 'description': 'Economic for better living', 'start_time': self.time_start1,
                                                                 'end_time': self.time_end1, 'location': 'KU', 'contact': '191'})
        meeting1 = Meeting.objects.filter(host=self.host_user).first()
        self.client.logout() #Host user has logged out.
        #Logged in User1.
        self.client.login(username='User1', password='isp123456')
        self.joining_url = reverse('appointment:join', args=(meeting1.id,))
        self.leaving_url = reverse('appointment:leave', args=(meeting1.id,))
        #User1 join meeting1.
        response = self.client.get(self.joining_url)
        response = self.client.get(self.leaving_url)
        self.client.logout() #User1 user has logged out.
        #Logged in Host.
        self.client.login(username='Host', password='isp123456')
        #Before kick
        response = self.client.get(reverse('appointment:participants', args=(meeting1.id,)))
        self.assertQuerysetEqual(response.context['participants'], [])
        response = self.client.get(reverse('appointment:kick', kwargs={'meeting_id': meeting1.id, 'user_id': self.user1.id}))
        messages = list(get_messages(response.wsgi_request))
        #Test message
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "This user doesn't joined yet.")
        #After kick
        response = self.client.get(reverse('appointment:participants', args=(meeting1.id,)))
        self.assertQuerysetEqual(response.context['participants'], [])