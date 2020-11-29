"""Test for create meeting form."""
import datetime
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.messages import get_messages


def create_user(username, email, password):
    """For create the user for test."""
    return User.objects.create_user(username=username, email=email, password=password)


class CreateMeetingFormTest(TestCase):
    """Class for test the form to create meeting."""

    def setUp(self):
        """Set up for the test."""
        self.user1 = create_user("User1", "User1@gmail.com", "isp123456")
        self.time_start1 = timezone.now()
        self.time_end1 = timezone.now() + datetime.timedelta(days=30)

    def test_try_to_access_create_meeting_page_with_unauthenticated_user(self):
        """The user have to login for access the create meeting page, if not redirect to the login page."""
        response = self.client.get(reverse('appointment:create-meeting'))
        self.assertEqual(response.status_code, 302)

    def test_try_to_access_create_meeting_page_with_authenticated_user(self):
        """The user have to login for access create meeting page."""
        self.client.post(reverse('login'), {'username': 'User1', 'password': 'isp123456'}, follow=True)
        response = self.client.get(reverse('appointment:create-meeting'))
        self.assertEqual(response.status_code, 200)

    def test_create_meeting_but_not_input_subject(self):
        """When create meeting the user should input the subject, if not input the subject still that page."""
        self.client.post(reverse('login'), {'username': 'User1', 'password': 'isp123456'}, follow=True)
        response = self.client.post(reverse('appointment:create-meeting'), {
                                    'description': 'Economic for better living', 'start_time': self.time_start1,
                                    'end_time': self.time_end1, 'location': 'KU', 'contact': '191'})
        self.assertEqual(response.status_code, 200)

    def test_create_meeting_but_not_input_description(self):
        """When create meeting the user should input the description, if not input the description still that page."""
        self.client.post(reverse('login'), {'username': 'User1', 'password': 'isp123456'}, follow=True)
        response = self.client.post(reverse('appointment:create-meeting'), {'subject': 'Econ',
                                                        'start_time': self.time_start1,
                                                        'end_time': self.time_end1, 'location': 'KU', 'contact': '191'})
        self.assertEqual(response.status_code, 200)

    def test_create_meeting_but_not_input_start_time(self):
        """When create meeting the user should input the start_time, if not input the start_time still that page."""
        self.client.post(reverse('login'), {'username': 'User1', 'password': 'isp123456'}, follow=True)
        response = self.client.post(reverse('appointment:create-meeting'), {'subject': 'Econ', 'description': 'Economic for better living',
                                                        'end_time': self.time_end1, 'location': 'KU', 'contact': '191'})
        self.assertEqual(response.status_code, 200)

    def test_create_meeting_but_not_input_end_time(self):
        """When create meeting the user should input the end_time, if not input the end_time still that page."""
        self.client.post(reverse('login'), {'username': 'User1', 'password': 'isp123456'}, follow=True)
        response = self.client.post(reverse('appointment:create-meeting'), {'subject': 'Econ', 'description': 'Economic for better living',
                                                        'start_time': self.time_start1, 'location': 'KU', 'contact': '191'})
        self.assertEqual(response.status_code, 200)

    def test_create_meeting_but_not_input_location(self):
        """When create meeting the user should input the location, if not input the location still that page."""
        self.client.post(reverse('login'), {'username': 'User1', 'password': 'isp123456'}, follow=True)
        response = self.client.post(reverse('appointment:create-meeting'), {'subject': 'Econ', 'description': 'Economic for better living',
                                                        'start_time': self.time_start1, 'end_time': self.time_end1, 'contact': '191'})
        self.assertEqual(response.status_code, 200)

    def test_create_meeting_but_not_input_contact(self):
        """When create meeting the user should input the contact, if not input the contact still that page."""
        self.client.post(reverse('login'), {'username': 'User1', 'password': 'isp123456'}, follow=True)
        response = self.client.post(reverse('appointment:create-meeting'), {'subject': 'Econ', 'description': 'Economic for better living',
                                                        'start_time': self.time_start1, 'end_time': self.time_end1, 'location': 'KU'})
        self.assertEqual(response.status_code, 200)

    def test_create_meeting_with_valid_input(self):
        """When create meeting with valid input it should create the meeting and redirect to home page."""
        self.client.post(reverse('login'), {'username': 'User1', 'password': 'isp123456'}, follow=True)
        response = self.client.post(reverse('appointment:create-meeting'), {'subject': 'Econ', 'description': 'Economic for better living',
                                                        'start_time': self.time_start1, 'end_time': self.time_end1, 'location': 'KU', 'contact': '191'})
        self.assertEqual(response.status_code, 302)

    def test_messages_when_create_meeting_form_is_valid(self):
        """When create meeting with valid input. It will shown the success messages."""
        self.client.post(reverse('login'), {'username': 'User1', 'password': 'isp123456'}, follow=True)
        response = self.client.post(reverse('appointment:create-meeting'), {'subject': 'Econ', 'description': 'Economic for better living',
                                                        'start_time': self.time_start1, 'end_time': self.time_end1, 'location': 'KU', 'contact': '191'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f"Econ was created successfully!!")