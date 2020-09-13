from django.test import TestCase
from .models import CustomUser
from http import HTTPStatus
# Create your tests here.


class TestCustomUser(TestCase):

    def test_signup(self):
        response = self.client.post(
                "/signup/",
                {
                    "username": "Jojo",
                    "email": "jojo.dio@zawarudo.com",
                    "password1": "itwasmedio",
                    "password2": "itwasmedio",
                },
            )
        print(response)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(CustomUser.objects.get(username="Jojo").exists())

    def test_login_username(self):
        self.client.post(
                "/signup/",
                {
                    "username": "Jojo",
                    "email": "jojo.dio@zawarudo.com",
                    "password1": "itwasmedio",
                    "password2": "itwasmedio",
                },
            )
        response = self.client.post(
            "/login/",
            {
                "email": "Jojo",
                "password": "itwasmedio",
            }
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_login_email(self):
        self.client.post(
                "/signup/",
                {
                    "username": "Jojo",
                    "email": "jojo.dio@zawarudo.com",
                    "password1": "itwasmedio",
                    "password2": "itwasmedio",
                },
            )
        response = self.client.post(
            "/login/",
            {
                "email": "jojo.dio@zawarudo.com",
                "password": "itwasmedio",
            }
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
