from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

def create_user(username, email, password):
    return User.objects.create_user(username=username,email=email,password=password)

class RegistrationTest(TestCase):
    """Class for test registration system"""

    def test_can_view_registration_page(self):
        """If we can access the registration page, status code should be 200 and use register.html template."""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_add_an_account_in_registration_page_with_valid_email(self):
        """If we have successfully created an account status of the response code should be 302 (redirect)."""
        response = self.client.post(reverse('register'), {'username':'User1','email':'User1@gmail.com','password1':'isp123456','password2':'isp123456'})
        self.assertEqual(response.status_code, 302)

    def test_can_not_registration_with_invalid_email(self):
        """If an email doesn't have @, it not an email, account creation failed."""
        response = self.client.post(reverse('register'), {'username':'User2','email':'User2 email','password1':'isp123456','password2':'isp123456'})
        self.assertEqual(response.status_code, 200)

    def test_can_not_registration_with_password_do_not_match_confirmation_password(self):
        """If password do not match with confirmation password, account creation failed."""
        response = self.client.post(reverse('register'), {'username':'User3','email':'User3@gmail.com','password1':'isp123456','password2':'isp234567'})
        self.assertEqual(response.status_code, 200)

    def test_can_not_registration_with_weak_password(self):
        """If password that too weak, account creation failed."""
        response = self.client.post(reverse('register'), {'username':'User4','email':'User4@gmail.com','password1':'12345678','password2':'12345678'})
        self.assertEqual(response.status_code, 200)

    def test_can_not_registration_with_that_username_already_exists(self):
        """Can not create an account, if we have that username"""
        create_user('User1', 'User1@gmail.com', 'isp123456')
        response = self.client.post(reverse('register'), {'username':'User1','email':'User6@gmail.com','password1':'isp123456','password2':'isp123456'})
        self.assertEqual(response.status_code, 200)

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

class LogOutTest(TestCase):
    """Class for test logout system"""

    def test_login_and_logout(self):
        """If you still login is_authenticated is true, if logout s_authenticated must be false"""
        create_user("User1", "User1@gmail.com", "isp123456")
        response = self.client.post(reverse('login'), {'username':'User1', 'password':'isp123456'}, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        response = self.client.get(reverse('logout'))
        self.assertFalse(response.context['user'].is_authenticated)
        