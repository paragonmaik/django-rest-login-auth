"""
Module for account app models tests.
"""
from django.test import TestCase
from account.models import User


class TestModels(TestCase):
    """
    Test models class.
    """

    def setUp(self):
        self.user1 = User.objects.create(
            name="Teste",
            email="teste@email.com",
            terms_conditions=True,
            password="Teste123**"
        )

        self.user2 = User.objects.create(
            name="Test2",
            email="testesuper@email.com",
            terms_conditions=True,
            password="Teste123**"
        )
        self.user2.is_admin = True
        self.user2.save()

    def test_user_is_created(self):
        """
        Tests if user is created and is saved to the database.
        """
        created_user = User.objects.get(email="teste@email.com")
        self.assertEqual(self.user1.email, created_user.email)

    def test_user_is_not_admin(self):
        """
        Tests if user is not saved as admin.
        """
        created_user = User.objects.get(email="teste@email.com")
        self.assertFalse(created_user.is_admin)

    def test_superuser_is_created(self):
        """
        Tests if superuser is created and is saved to the database.
        """
        created_superuser = User.objects.get(email="testesuper@email.com")
        self.assertEqual(self.user2.email, created_superuser.email)

    def test_superuser_is_admin(self):
        """
        Tests if superuser is saved as admin.
        """
        created_superuser = User.objects.get(email="testesuper@email.com")
        self.assertTrue(created_superuser.is_admin)
