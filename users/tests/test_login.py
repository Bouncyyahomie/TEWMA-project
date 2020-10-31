from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

def create_user(username, email, password):
    return User.objects.create_user(username=username,email=email,password=password)

class LogInTest(TestCase):
    """Class for test login system"""

    def test_simple_login(self):
        """If can login, that user must be authenticated in website"""
        create_user("User1", "User1@gmail.com", "isp123456")
        response = self.client.post(reverse('login'), {'username':'User1', 'password':'isp123456'}, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_can_not_login_with_user_that_not_enter_password(self):
        """Can not login with enter the username but not enter the password"""
        create_user("User1", "User1@gmail.com", "isp123456")
        response = response = self.client.post(reverse('login'), {'username':'User1'}, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_can_not_login_with_user_that_enter_wrong_password(self):
        """Can not login, if enter the wrong password"""
        create_user("User1", "User1@gmail.com", "isp123456")
        response = self.client.post(reverse('login'), {'username':'User1', 'password':'isp555555'}, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)