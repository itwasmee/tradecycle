from django.test import TestCase
from django.urls import reverse
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
                'title': 'testing the contact form',
                'message': 'Hello World'
            }
        )
        self.assertEqual(response.status_code, 302)
