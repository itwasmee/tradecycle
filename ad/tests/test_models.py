from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Ad

myclient = Client()


class TestAdModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            email='jojo@dio.com',
            username='Jojo',
            password='itwasmedio'
        )
        myclient.login(username='Jojo', password='itwasmedio')
        with open('ad/tests/1.jpg', 'rb') as data:
            cls.ad = Ad(
                title='marc de cafe',
                action='O',
                user_id=cls.user,
                description='Je donne du marc de cafe',
                image=data,
                city='Paris'
                )
        data.close()

    def test_string_representation(self):
        self.assertEqual(str(self.ad), self.ad.title)
