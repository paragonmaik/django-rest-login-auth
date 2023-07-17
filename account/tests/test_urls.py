"""
Module for account app URLs tests.
"""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from account.views import UserRegistrationView, UserLoginView, UserPasswordChangeView


class TestUrls(SimpleTestCase):
    """
    Tests account app URLs.
    ...
    Methods:
        test_register_url_resolves():
            Tests register/ URL.

        test_login_url_resolves():
            Tests login/ URL.
    """

    def test_register_url_resolves(self):
        """
        Tests register/ URL.
        """
        url = reverse("register")
        self.assertEqual(resolve(url).func.view_class, UserRegistrationView)

    def test_login_url_resolves(self):
        """
        Tests login/ URL.
        """
        url = reverse("login")
        self.assertEqual(resolve(url).func.view_class, UserLoginView)

    def test_password_change_url_resolves(self):
        """
        Tests password-change/ URL.
        """
        url = reverse("password_change")
        self.assertEqual(resolve(url).func.view_class, UserPasswordChangeView)
