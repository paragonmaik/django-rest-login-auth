from django.test import TestCase, Client
from django.urls import reverse
from account.models import User
import json


class TestViews(TestCase):
    """
    Test views class
    """

    def setUp(self) -> None:
        """
        Sets up test client and testing URLs
        """
        self.client = Client()
        self.register_url = reverse("register")

    def test_successful_user_register_POST(self):
        """
        Test if user can be registered successfully
        """
        response = self.client.post(self.register_url, {
            "name": "Teste",
            "email": "email@example.com",
            "password": "Teste123@@",
            "password2": "Teste123@@",
            "terms_conditions": "True"
        })
        response_body = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_body["message"], "Registered!")
        self.assertTrue("token" in response_body)
