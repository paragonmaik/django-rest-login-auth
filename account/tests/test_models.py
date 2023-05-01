from django.test import TestCase
from account.models import User


class TestModels(TestCase):
    """
    Test models class
    """

    def setUp(self):
        self.user1 = User.objects.create(
            name="Teste",
            email="teste@email.com",
            terms_conditions=True,
            password="Teste123**"
        )

    def test_user_is_created(self):
        """
        Tests if user is created and is saved to the database
        """
        created_user = User.objects.get(email="teste@email.com")
        self.assertEqual(self.user1.email, created_user.email)
