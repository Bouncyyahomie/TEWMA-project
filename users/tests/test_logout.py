"""Test for User logout."""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


def create_user(username, email, password):
    """For create the user for test."""
    return User.objects.create_user(username=username, email=email, password=password)


class LogOutTest(TestCase):
    """Class for test logout system."""

    def test_login_and_logout(self):
        """If you still login is_authenticated is true, if logout s_authenticated must be false."""
        create_user("User1", "User1@gmail.com", "isp123456")
        response = self.client.post(reverse('login'), {'username': 'User1', 'password': 'isp123456'}, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        response = self.client.get(reverse('logout'))
        self.assertFalse(response.context['user'].is_authenticated)
