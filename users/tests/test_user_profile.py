from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import Profile


def create_user(username, email, password):
    """For create the user for test"""
    user = User.objects.create_user(username=username, email=email, password=password)
    user.set_password(password)
    user.save()
    return user


class ProfileTest(TestCase):
    """Test User profile"""

    def setUp(self):
        """Setup for test"""
        self.user1 = create_user("User1", "User1@gmail.com", "isp123456")
        self.user1_profile = Profile.objects.filter(user=self.user1).first()
        self.profile_url = reverse('profile')

    def test_is_created_user_has_a_profile(self):
        """When the user has been created. The user must has a profile"""
        self.assertEqual(str(self.user1_profile), "Profile of User1")

    def test_default_picture_in_user_profile(self):
        """Default image must be anonymous.png"""
        self.assertEqual(self.user1_profile.image.name, "anonymous.png")

    def test_try_to_access_to_user_profile_with_unauthenticated_user(self):
        """Unauthenticated user can't see the profile page"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login/?next=/profile/")

    def test_try_to_access_to_user_profile_with_authenticated_user(self):
        """Authenticated user can see their profile page"""
        self.client.login(username='User1', password='isp123456')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
