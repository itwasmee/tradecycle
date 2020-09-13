from django.test import TestCase
from django.urls import reverse
from accounts.models import CustomUser
# Create your tests here.


class TestHomePageView(TestCase):
    def test_homepage(self):
        response = self.client.get(reverse('accueil'))
        self.assertEqual(response.status_code, 200)


class TestAboutPageView(TestCase):
    def test_aboutpage(self):
        response = self.client.get(reverse('a-propos'))
        self.assertEqual(response.status_code, 200)


class TestContactPageView(TestCase):
    def test_contactpage(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)

    def test_contactform(self):
        response = self.client.post(
            'contact',
            {
                'email': 'tradecycle@tradecycle.fr',
                'subject': 'testing the contact form',
                'message': 'Hello World'
            }
        )
        self.assertEqual(response.status_code, 300)


class TestProfilePageView(TestCase):
    def setUp(self):
        self.client.post(
            "/signup/",
            {
                "username": "Jojo",
                "email": "jojo.dio@zawarudo.com",
                "password1": "itwasmedio",
                "password2": "itwasmedio",
            },
        )
        self.client.post(
            "/login/",
            {
                "email": "jojo.dio@zawarudo.com",
                "password": "itwasmedio",
            }
        )

    def test_profilepage(self):
        print(CustomUser.objects.get(username='Jojo').id)
        response = self.client.get(
            reverse(
                'profil', args={
                    "slug": CustomUser.objects.get(username='Jojo').id
                    }
                )
            )
        print(response)
        self.assertEqual(response.status_code, 200)
