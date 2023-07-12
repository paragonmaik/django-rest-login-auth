"""
Module for account app views tests.
"""
import json
from django.test import TestCase, Client
from django.urls import reverse
from account.models import User


class TestRegisterView(TestCase):
    """
    Tests register views.
    """

    def setUp(self) -> None:
        """
        Sets up test client and testing URLs.
        """
        self.client = Client()
        self.register_url = reverse("register")

    def test_successful_user_register_post(self):
        """
        Test if user can be registered successfully.
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

    def test_unsuccessful_user_register_post(self):
        """
        Test if user can't be registered with invalid data.
        """
        response = self.client.post(self.register_url, {
            "name": "",
            "email": "email@example.com",
            "password": "Teste123@@",
            "password2": "Teste123@@",
            "terms_conditions": "True"
        })

        response_body = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, 422)
        self.assertTrue("errors" in response_body)


class TestAdminRegisterView(TestCase):
    """
    Tests admin registration view.
    """

    def setUp(self) -> None:
        """
        Sets up test client and testing URLs.
        """
        self.client = Client()
        self.register_url = reverse("register_admin")

    def test_successful_admin_register_post(self):
        """
        Test if admin can be registered successfully.
        """
        response = self.client.post(self.register_url, {
            "name": "Admin",
            "email": "Admin@example.com",
            "password": "Teste123@@",
            "password2": "Teste123@@",
            "terms_conditions": "True",
        })


class TestLoginView(TestCase):
    """
    Tests login views.
    """

    def setUp(self) -> None:
        """
        Sets up test client and testing URLs.
        """
        self.client = Client()
        self.login_url = reverse("login")
        self.user1 = User.objects.create_user(
            name="Teste",
            email="teste@email.com",
            terms_conditions=True,
            password="Teste123**"
        )

    def test_sucessful_login_post(self):
        """
        Tests if user can be logged in successfully.
        """
        response = self.client.post(self.login_url, {
            "email": "teste@email.com",
            "password": "Teste123**"
        })

        response_body = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_body["message"], "Logged in!")
        self.assertTrue("token" in response_body)

    def test_unsuccessful_login_missing_data_post(self):
        """
        Test if user can't log in with missing data.
        """
        response = self.client.post(self.login_url, {
            "email": "teste@email.com",
            "password": ""
        })

        response_body = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, 401)
        self.assertTrue("errors" in response_body)

    def test_unsuccessful_login_invalid_field_post(self):
        """
        Test if user can't log with invalid data.
        """
        response = self.client.post(self.login_url, {
            "email": "teste@email.com",
            "password": "wrong_password"
        })

        response_body = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, 404)
        self.assertTrue("errors" in response_body)
