from django.test import TestCase
from account.models import UserManager, User


class TestModels(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(
            name="Teste",
            email="teste@email.com",
            terms_conditions=True,
            password="Teste123**"
        )

    def test_user_is_created(self):
        created_user = User.objects.get(email="teste@email.com")
        self.assertEqual(self.user1.email, created_user.email)
