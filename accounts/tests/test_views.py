from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client

myclient = Client()


class TestSignupView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.response = myclient.post(
                "/signup/",
                {
                    "username": "Jojo",
                    "email": "jojo.dio@zawarudo.com",
                    "password1": "itwasmedio",
                    "password2": "itwasmedio",
                },
                follow=True
            )

    def test_response_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_user_is_created(self):
        user = get_user_model().objects.filter(username='Jojo')
        self.assertTrue(user.exists())

    def test_data_match(self):
        user = get_user_model().objects.get(username='Jojo')
        self.assertEqual(
            [user.username, user.email],
            ['Jojo', 'jojo.dio@zawarudo.com']
            )
        user.check_password('itwasmedio')


class TestLoginEmailView(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(
            username='Jojo',
            password='itwasmedio',
            email='jojo@dio.com'
            )
        cls.email_response = myclient.post(
            "/login/",
            {
                "username": "jojo@dio.com",
                "password": "itwasmedio",
            },
            follow=True
        )

    def test_user_exists(self):
        user = get_user_model().objects.filter(username='Jojo')
        self.assertTrue(user.exists())

    def test_login_email_status_code(self):
        self.assertEqual(self.email_response.status_code, 200)

    def test_login_email_is_auth(self):
        self.assertEqual(self.email_response.context['user'].username, 'Jojo')


class TestLoginUsernameView(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(
            username='Jojo',
            password='itwasmedio',
            email='jojo@dio.com'
            )
        cls.username_response = myclient.post(
                "/login/",
                {
                    "username": "Jojo",
                    "password": "itwasmedio",
                },
                follow=True
            )

    def test_user_exists(self):
        user = get_user_model().objects.filter(username='Jojo')
        self.assertTrue(user.exists())

    def test_login_username_status_code(self):
        self.assertEqual(self.username_response.status_code, 200)

    def test_login_username_is_auth(self):
        self.assertEqual(self.username_response.context['user'].username, 'Jojo')
