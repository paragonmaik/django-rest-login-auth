from django.test import SimpleTestCase
from django.urls import reverse, resolve
from account.views import UserRegistrationView


class TestUrls(SimpleTestCase):
    def test_register_url_resolves(self):
        url = reverse("register")
        self.assertEqual(resolve(url).func.view_class, UserRegistrationView)
