from shutil import rmtree

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Ad

myclient = Client()


class TestAdPostView(TestCase):
    @classmethod
    def setUpTestData(cls):
        rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        cls.resp = get_user_model().objects.create_user(
            username='joey',
            password='itwasmedio',
            email='jojo@dio.com'
            )
        myclient.login(username='joey', password='itwasmedio')
        with open('ad/tests/1.jpg', 'rb') as img:
            cls.response = myclient.post(
                '/deposer-une-annonce/',
                {
                    'action': 'O',
                    'title': 'cafe',
                    'description': 'donne cafe',
                    'image': img,
                    'city': 'Paris',
                },
                follow=True
            )
        img.close()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def test_redirect_after_submit(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed('merci-annonce.html')

    def test_ad_saved(self):
        self.assertEqual(Ad.objects.get(title='cafe').title, 'cafe')

    # test if correct template is used
    def test_correct_template(self):
        self.assertTemplateUsed('deposer-une-annonce.html')

    # test only one ad has been posted
    def test_ad_posted_once(self):
        self.assertEqual(Ad.objects.filter(title='cafe').count(), 1)

    # test datat corresponds
    def test_data_is_same(self):
        ad = Ad.objects.get(title='cafe')
        data = [
            ad.title,
            ad.action,
            ad.description,
            ad.city, ad.user_id.username,
            ]
        self.assertEqual(
            data, [
                'cafe',
                'O',
                'donne cafe',
                'Paris',
                (get_user_model().objects.get(username='joey').username),
                ]
            )

    # test redirect if user is not logged in
    def test_redirect_if_anonymous(self):
        self.client.logout()
        with open('ad/tests/1.jpg', 'rb') as data:
            self.anonymous_response = self.client.post(
                '/deposer-une-annonce/',
                {
                    'action': 'O',
                    'title': 'terre',
                    'description': 'donne terre',
                    'image': data,
                    'city': 'Lyon',
                },
                follow=True
            )
        data.close()
        self.assertEqual(self.anonymous_response.status_code, 200)
        self.assertTemplateUsed('login.html')
        self.assertFalse(Ad.objects.filter(title='terre').exists())


class TestDeleteAdView(TestCase):
    @classmethod
    def setUpTestData(cls):
        rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        cls.resp = get_user_model().objects.create_user(
            username='jojo',
            password='itwasmedio',
            email='jojo@dio.com'
            )
        myclient.login(username='jojo', password='itwasmedio')
        with open('ad/tests/1.jpg', 'rb') as data:
            cls.ad_post_response = myclient.post(
                '/deposer-une-annonce/',
                {
                    'action': 'O',
                    'title': 'cafe',
                    'description': 'donne cafe',
                    'image': data,
                    'city': 'Paris',
                },
                follow=True
            )
        data.close()
        ad = Ad.objects.get(title='cafe')
        cls.ad_delete_response = myclient.post(
            f'/delete_ad/{ad.id}'
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    # test template
    def test_correct_template(self):
        self.assertTemplateUsed('profile.html')

    # test status_code
    def test_post_status_code(self):
        self.assertEqual(self.ad_post_response.status_code, 200)

    # test status_code for delete
    def test_deletion_status_code(self):
        self.assertEqual(self.ad_delete_response.status_code, 200)

    def test_ad_is_deleted(self):
        self.assertFalse(Ad.objects.filter(title='cafe').exists(), True)


class TestDetailAdView(TestCase):
    @classmethod
    def setUpTestData(cls):
        rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        cls.resp = get_user_model().objects.create_user(
            username='jojo',
            password='itwasmedio',
            email='jojo@dio.com'
            )
        myclient.login(username='jojo', password='itwasmedio')
        with open('ad/tests/1.jpg', 'rb') as data:
            cls.ad_post_response = myclient.post(
                '/deposer-une-annonce/',
                {
                    'action': 'O',
                    'title': 'cafe',
                    'description': 'donne cafe',
                    'image': data,
                    'city': 'Paris',
                },
                follow=True
            )
        data.close()
        ad = Ad.objects.get(title='cafe')
        cls.ad_get_response = myclient.get(f'/ad/{ad.id}')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def test_template_used(self):
        self.assertTemplateUsed('ad.html')

    def test_status_code(self):
        self.assertEqual(self.ad_get_response.status_code, 200)

    def test_context_match(self):
        self.assertContains(self.ad_get_response, 'cafe')


class TestFavoritesView(TestCase):
    @classmethod
    def setUpTestData(cls):
        rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        cls.resp = get_user_model().objects.create_user(
            username='jojo',
            password='itwasmedio',
            email='jojo@dio.com'
            )
        myclient.login(username='jojo', password='itwasmedio')
        with open('ad/tests/1.jpg', 'rb') as data:
            cls.ad_post_response = myclient.post(
                '/deposer-une-annonce/',
                {
                    'action': 'O',
                    'title': 'cafe',
                    'description': 'donne cafe',
                    'image': data,
                    'city': 'Paris',
                },
                follow=True
            )
        data.close()
        cls.ad_id = Ad.objects.get(title='cafe').id
        cls.favs_response = myclient.get('/favoris/')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    # status code
    def test_status_code(self):
        self.assertEqual(self.favs_response.status_code, 200)

    # check if empty by default
    def test_empty(self):
        self.assertEqual(self.favs_response.context["empty"], True)

    # template
    def test_template_used(self):
        self.assertTemplateUsed('favoris.html')

    # check if favorites added
    def test_fav_displays(self):
        myclient.post(f'/fav_ad/{self.ad_id}', {})
        favs_response = myclient.get('/favoris/')
        self.assertEqual(favs_response.context["favs"][0].ad.title, "cafe")


class TestFavoritesAddView(TestCase):
    @classmethod
    def setUpTestData(cls):
        rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        cls.resp = get_user_model().objects.create_user(
            username='jojo',
            password='itwasmedio',
            email='jojo@dio.com'
            )
        myclient.login(username='jojo', password='itwasmedio')
        with open('ad/tests/1.jpg', 'rb') as data:
            cls.ad_post_response = myclient.post(
                '/deposer-une-annonce/',
                {
                    'action': 'O',
                    'title': 'cafe',
                    'description': 'donne cafe',
                    'image': data,
                    'city': 'Paris',
                },
                follow=True
            )
        data.close()
        cls.ad = Ad.objects.get(title='cafe')
        cls.fav_ad_response = myclient.post(f'/fav_ad/{cls.ad.id}')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    # check status code
    def test_status_code(self):
        self.assertEqual(self.fav_ad_response.status_code, 200)

    # check favorite is added and deleted
    def test_fav_added(self):
        favs_response = myclient.get('/favoris/')
        self.assertEqual(favs_response.context["favs"][0].ad.title, "cafe")

    def test_fav_removed(self):
        myclient.post(f'/fav_ad/{self.ad.id}')
        favs_response = myclient.get('/favoris/')
        self.assertEqual(favs_response.context["empty"], True)
