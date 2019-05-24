from django.test import TestCase
from User.models import User


class UserModel(TestCase):
    def test_creation(self) -> None:
        email: str = 'az@er.ty'
        password: str = 'azerty'
        firstname: str = 'Azerty'
        user: User = User.objects.create_user(
            email=email, password=password, firstname=firstname
        )
        inserted_user: User = User.objects.first()  # type: ignore
        self.assertEqual(user, inserted_user)
        self.assertEqual(email, inserted_user.email)
        self.assertTrue(inserted_user.check_password(password))
        self.assertEqual(firstname, inserted_user.firstname)
