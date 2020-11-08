"""Test for User registration."""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages


def create_user(username, email, password):
    """For create the user for test."""
    return User.objects.create_user(username=username, email=email, password=password)


class RegistrationTest(TestCase):
    """Class for test registration system."""

    def test_can_view_registration_page(self):
        """If we can access the registration page, status code should be 200 and use register.html template."""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_add_an_account_in_registration_page_with_valid_email(self):
        """If we have successfully created an account status of the response code should be 302 (redirect)."""
        response = self.client.post(reverse('register'), {
                                    'username': 'User1', 'email': 'User1@gmail.com', 'password1': 'isp123456',
                                    'password2': 'isp123456'})
        self.assertEqual(response.status_code, 302)

    def test_can_not_registration_with_invalid_email(self):
        """If an email doesn't have @, it not an email, account creation failed."""
        response = self.client.post(
            reverse('register'), {'username': 'User2', 'email': 'User2 email',
                                  'password1': 'isp123456', 'password2': 'isp123456'})
        self.assertEqual(response.status_code, 200)

    def test_can_not_registration_with_password_do_not_match_confirmation_password(self):
        """If password do not match with confirmation password, account creation failed."""
        response = self.client.post(reverse('register'), {
                                    'username': 'User3', 'email': 'User3@gmail.com', 'password1': 'isp123456',
                                    'password2': 'isp234567'})
        self.assertEqual(response.status_code, 200)

    def test_can_not_registration_with_weak_password(self):
        """If password that too weak, account creation failed."""
        response = self.client.post(reverse('register'), {
                                    'username': 'User4', 'email': 'User4@gmail.com', 'password1': '12345678',
                                    'password2': '12345678'})
        self.assertEqual(response.status_code, 200)

    def test_can_not_registration_with_that_username_already_exists(self):
        """Can not create an account, if we have that username."""
        create_user('User1', 'User1@gmail.com', 'isp123456')
        response = self.client.post(reverse('register'), {
                                    'username': 'User1', 'email': 'User6@gmail.com', 'password1': 'isp123456',
                                    'password2': 'isp123456'})
        self.assertEqual(response.status_code, 200)

    def test_response_code_when_authenticated_user_try_to_access_register_page(self):
        """Authenticated user try to access to registration page, it should redirect to home page."""
        create_user("User1", "User1@gmail.com", "isp123456")
        self.client.post(reverse('login'), {'username': 'User1', 'password': 'isp123456'}, follow=True)
        response = self.client.post(reverse('register'))
        self.assertEqual(response.status_code, 302)

    def test_register_messages_when_user_authenticated(self):
        """When authenticated user try to access to registration page. Show the message for the user."""
        create_user("User1", "User1@gmail.com", "isp123456")
        self.client.post(reverse('login'), {'username': 'User1', 'password': 'isp123456'}, follow=True)
        response = self.client.post(reverse('register'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You have to logout before make a new register')
