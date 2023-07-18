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
    ...
    Methods:
        setUp():
            Sets test client and URL variables.

        test_successful_user_register_post():
            Tests successful register post.

        test_unsuccessful_user_register_post():
            Tests unsuccessful register post.
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


class TestLoginView(TestCase):
    """
    Tests login views.
    ...
    Methods:
        setUp():
            Sets test client and URL variables.

        test_sucessful_login_post():
            Tests successful login post.

        test_unsuccessful_login_missing_data_post():
            Tests unsuccessful login post.

        test_unsuccessful_login_invalid_field_post():
            Tests unsuccessful login post.
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
        self.assertEqual(response.status_code, 401)
        self.assertTrue("errors" in response_body)


class TestPasswordChangeView(TestCase):
    """
    Tests password change views.
    ...
    Methods:
        setUp():
            Sets test client and URL variables.

        test_successful_password_change():
            Tests successful password change post.

        test_unsuccessful_password_change():
            Tests unsuccessful password change post.
    """

    def setUp(self) -> None:
        """
        Sets up test client and testing URLs.
        """
        self.client = Client()
        self.login_url = reverse("login")
        self.change_password_url = reverse("password_change")
        self.user1 = User.objects.create_user(
            name="Teste",
            email="teste@email.com",
            terms_conditions=True,
            password="Teste123**"
        )

        response_login = self.client.post(self.login_url, {
            "email": "teste@email.com",
            "password": "Teste123**"
        })

        response_body_login = json.loads(
            response_login.content.decode("utf-8"))

        self.token = response_body_login["token"]["access"]

    def test_successful_password_change(self):
        """
        Tests if password is changed sucessfully.
        """
        headers = {
            "HTTP_AUTHORIZATION": "Bearer " + self.token}

        response = self.client.post(self.change_password_url, {
            "password": "Newpassword123**",
            "password2": "Newpassword123**"
        }, content_type="application/json",
            **headers)

        response_body = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_body["message"],
                         "Password was changed successfully.")

    def test_unsuccessful_password_change(self):
        """
        Tests if user is unable to change passwords that don't match.
        """
        headers = {
            "HTTP_AUTHORIZATION": "Bearer " + self.token}

        response = self.client.post(self.change_password_url, {
            "password": "Newpassword123**",
            "password2": "Newpassword"
        }, content_type="application/json",
            **headers)

        response_body = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, 401)
        self.assertTrue("errors" in response_body)


class TestPasswordResetEmailView(TestCase):
    """
    Tests password reset email views.
    ...
    Methods:
        setUp():
            Sets test client and URL variables.

        test_successful_password_reset_email():
            Tests successful password email post.

        test_unsuccessful_password_reset_email():
            Tests unsuccessful password email post.
    """

    def setUp(self) -> None:
        self.client = Client()
        self.reset_password_url = reverse("send_reset_password_email")
        self.user1 = User.objects.create_user(
            name="Teste",
            email="teste@email.com",
            terms_conditions=True,
            password="Teste123**"
        )

    def test_successful_password_reset_email(self):
        """
        Tests if password reset email is requested with valid data.
        """
        response = self.client.post(self.reset_password_url, {
            "email": self.user1.email
        })

        response_body = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_body["message"],
                         "If the given email belongs to a user, a reset link will be sent.")

    def test_unsucessful_password_reset_email(self):
        """
        Tests if password reset email is not requested with invalid data.
        """
        response = self.client.post(self.reset_password_url, {
            "email": self.user1.email
        })

        response_body = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_body["message"],
                         "If the given email belongs to a user, a reset link will be sent.")
