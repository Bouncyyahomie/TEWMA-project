"""Views Tests"""
from django.test import TestCase
from django.urls import reverse


class IndexViewTest(TestCase):
    """Test for TewMa home page."""

    def test_check_default_home_page(self):
        """If user is not authenticated, show Welcome, AnonymousUser"""
        response = self.client.get(reverse('appointment:home_page'))
        self.assertContains(response, "Welcome, AnonymousUser")
