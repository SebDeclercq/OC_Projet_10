from typing import Dict, Optional
from unittest import skip
from django.http import HttpResponse
from django.test import Client, TestCase
from django.urls import resolve
from User.models import User
from User.views import LoginView


class LogInViewTest(TestCase):
    URL: str = '/user/login'

    def setUp(self) -> None:
        self.client: Client = Client()
        self.valid_password: str = 'azerty'
        self.user: User = User.objects.create_user(
            email='az@er.ty', password=self.valid_password
        )

    def test_url_resolve_login(self) -> None:
        self.assertEqual(
            resolve(self.URL).func.view_class, LoginView  # type: ignore
        )

    def test_page_return_expected_html(self) -> None:
        response: HttpResponse = self.client.get(self.URL)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_valid_credentials(self) -> None:
        response: HttpResponse = self.client.post(self.URL, {
            'email': self.user.email, 'password': self.valid_password
        })
        self.assertRedirects(response, '/')

    def test_login_invalid_credentials(self) -> None:
        response: HttpResponse = self.client.post(self.URL, {
            'email': self.user.email, 'password': 'wrong_password'
        })
        self.assertTemplateUsed(response, 'login.html')


class SignUpModelTest(TestCase):
    def test_user_manage_create_user(self) -> None:
        user: User = User.objects.create_user(
            email='az@er.ty', password='azerty',
            name='Uiop', firstname='Azerty'
        )
        inserted_user: Optional[User] = User.objects.first()
        if inserted_user is not None:
            self.assertEqual(inserted_user, user)
            self.assertEqual(inserted_user.get_full_name(),
                             'Azerty Uiop')

    def test_user_manager_create_superuser(self) -> None:
        superuser: User = User.objects.create_superuser(
            email='az@er.ty', password='azerty'
        )
        self.assertEqual(User.objects.first(), superuser)

    def test_user_manager_create_superuser_attrs(self) -> None:
        User.objects.create_superuser(
            email='az@er.ty', password='azerty'
        )
        superuser: Optional[User] = User.objects.first()
        if superuser is not None:
            self.assertEqual(superuser.is_superuser, True)
            self.assertEqual(superuser.is_staff, True)


class SignUpViewTest(TestCase):
    URL: str = '/user/signup'
    SUCCESS_URL: str = '/'

    def setUp(self) -> None:
        self.client: Client = Client()
        self.data: Dict[str, str] = {
            'firstname': 'Azerty',
            'password1': 'azerty',
            'password2': 'azerty',
            'email': 'az@er.ty'
        }

    def test_page_return_expected_html(self) -> None:
        response: HttpResponse = self.client.get(self.URL)
        self.assertTemplateUsed(response, 'signup.html')

    def test_new_user_sign_up(self) -> None:
        response: HttpResponse = self.client.post(self.URL, data=self.data,
                                                  follow=True)
        self.assertIn((self.SUCCESS_URL, 302), response.redirect_chain)

    def test_new_user_sign_up_insertion(self) -> None:
        self.client.post(self.URL, data=self.data)
        user: Optional[User] = User.objects.first()
        if user is not None:
            self.assertEqual(user.email, self.data['email'])
            self.assertTrue(user.check_password(self.data['password1']))

    @skip('No behaviour has been set up for password mismatch')
    def test_bad_form_completion(self) -> None:
        data: Dict[str, str] = self.data.copy()
        data['password2'] = 'xxx'
        r: HttpResponse = self.client.post(self.URL, data=data)
        self.assertIn('Password mismatch', r.content.decode('utf-8'))


class LogOutViewTest(TestCase):
    URL: str = '/user/logout'
    LOGIN_URL: str = '/user/login'

    def setUp(self) -> None:
        self.client: Client = Client()
        user: User = User.objects.create_user(
            email='az@er.ty', password='azerty'
        )
        self.client.post(self.LOGIN_URL, {
            'email': user.email, 'password': 'azerty'
        })

    def test_logout(self) -> None:
        response: HttpResponse = self.client.get(self.URL, follow=True)
        self.assertRedirects(response, '/')
