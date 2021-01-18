from shutil import rmtree

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Profile


class TestProfileModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        get_user_model().objects.create_user(
            username='jojo',
            email='jojo@dio.com',
            password='itwasmedio'
            )
        cls.user = get_user_model().objects.get(username='jojo')
        cls.profile = Profile(user=cls.user)
        cls.profile.activity = 'agriculture'
        cls.profile.location = 'paris'
        with open("ad/tests/1.jpg", "rb") as data:
            cls.profile.picture = data
        data.close()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def test_str_model(self):
        self.assertEqual(str(Profile.objects.get(user=self.user)), 'jojo\'s profile')

    def test_profile_data(self):
        self.assertEqual(
            [self.profile.user, self.profile.activity, self.profile.location],
            [self.user, 'agriculture', 'paris']
            )
