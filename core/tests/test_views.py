from shutil import rmtree

from ad.models import Ad
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..models import Profile


class TestHomePageView(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse("accueil"))

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed("accueil.html")


class TestAboutPageView(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse("a-propos"))

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed("a-propos.html")


class TestContactPageView(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse("contact"))

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed("contact.html")

    def test_contactform(self):
        response = self.client.post(
            "/contact/",
            {
                "email": "tradecycle@tradecycle.fr",
                "subject": "testing the contact form",
                "message": "Hello World",
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)


class TestProfileCreation(TestCase):
    def test_no_profile(self):
        get_user_model().objects.all().delete()
        profiles = Profile.objects.all()
        self.assertLess(profiles.count(), 1)

    def test_profile_created(self):
        get_user_model().objects.create_user(
            username="Jojo",
            email="jojo@dio.com",
            password="itwasmedio",
        )
        profiles = Profile.objects.all()
        self.assertTrue(profiles.exists())


class TestLoggedIn(TestCase):
    def setUp(self):
        rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        get_user_model().objects.create_user(
            username="Jojo",
            email="jojo@dio.com",
            password="itwasmedio",
        )
        self.client.login(username='Jojo', password='itwasmedio')
        self.response = self.client.get("/profil/")

    def tearDown(self):
        rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_user_is_logged_in(self):
        self.assertEqual(self.response.context["user"].username, "Jojo")

    def test_template(self):
        self.assertTemplateUsed("profil.html")

    def test_content_match(self):
        self.assertContains(self.response, text="Jojo")


class TestLoggedOut(TestCase):
    def setUp(self):
        self.client.logout()
        self.response = self.client.get("/profil/", follow=True)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_redirect_anonymous(self):
        self.assertTemplateUsed("login.html")


class TestPostedAds(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(
            username="joey",
            email="joey@joestar.com",
            password="itwasmedio",
        )
        self.client.login(username='joey', password='itwasmedio')
        with open("ad/tests/1.jpg", "rb") as img_one:
            self.client.post(
                "/deposer-une-annonce/",
                {
                    "action": "O",
                    "title": "cafe",
                    "description": "donne cafe",
                    "image": img_one,
                    "city": "Paris",
                },
            )
        img_one.close()
        with open("ad/tests/1.jpg", "rb") as img_two:
            self.client.post(
                "/deposer-une-annonce/",
                {
                    "action": "C",
                    "title": "Terreau",
                    "description": "donne terreau",
                    "image": img_two,
                    "city": "Rennes",
                },
            )
        img_two.close()
        self.response = self.client.get("/profil/")

    def test_context_match(self):
        self.assertContains(self.response, "cafe", status_code=200)
        self.assertContains(self.response, "Terreau", status_code=200)


class TestDeletedAd(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(
            username="joey",
            email="joey@joestar.com",
            password="itwasmedio",
        )
        self.client.login(username='joey', password='itwasmedio')
        with open("ad/tests/1.jpg", "rb") as img_one:
            self.client.post(
                "/deposer-une-annonce/",
                {
                    "action": "O",
                    "title": "cafe",
                    "description": "donne cafe",
                    "image": img_one,
                    "city": "Paris",
                },
            )
        img_one.close()
        ad = Ad.objects.get(title='cafe')
        ad.delete()
        self.response = self.client.get("/profil/")

    def test_ad_doesnt_show(self):
        self.assertNotContains(self.response, "donne cafe")


class TestProfileCustomisation(TestCase):
    def setUp(self):
        rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        get_user_model().objects.create_user(
            username="joey",
            email="joey@joestar.com",
            password="itwasmedio",
        )
        self.client.login(username="joey@joestar.com", password="itwasmedio")
        self.response = self.client.get("/profil/")
        with open("ad/tests/1.jpg", "rb") as data:
            self.post_response = self.client.post(
                "/profil/",
                {"pictrure": data, "location": "Caen", "activity": "Agriculture"},
                follow=True
            )
        data.close()
        self.get_response = self.client.get("/profil/")

    def tearDown(self):
        rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def test_status_code(self):
        self.assertEqual(self.post_response.status_code, 200)

    def test_context_matches(self):
        self.assertContains(self.get_response, text="Caen")
        self.assertContains(self.get_response, text="Agriculture")

    def test_empty_post(self):
        response = self.client.post(
            "/profil/",
            {"pictrure": "", "location": "", "activity": ""},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.get_response = self.client.get("/profil/")
        self.assertContains(self.get_response, text="Caen")
        self.assertContains(self.get_response, text="Agriculture")

    def test_change_field(self):
        response = self.client.post(
            "/profil/", {"location": "Lyon"}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Caen")
        self.assertContains(response, "Lyon")
