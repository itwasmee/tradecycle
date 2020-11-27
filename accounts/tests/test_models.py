from django.test import TestCase
from django.contrib.auth import get_user_model


class TestCustomUser(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(
            email='jojo@dio.com',
            username='jojo',
            password='itwasmedio'
        )
        print('Hello')

    def test_email(self):
        user = get_user_model().objects.get(username='jojo')
        expected_object = f'{user.email}'
        assert expected_object == 'jojo@dio.com'

    def test_username(self):
        user = get_user_model().objects.get(username='jojo')
        expected_object = f'{user.username}'
        assert expected_object == 'jojo'

    def test_password(self):
        user = get_user_model().objects.get(username='jojo')
        assert user.check_password('itwasmedio') is True
