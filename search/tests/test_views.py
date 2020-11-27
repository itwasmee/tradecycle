from django.test import TestCase
from shutil import rmtree
from django.conf import settings
from django.contrib.auth import get_user_model
from ad.models import Ad


class TestSearchView(TestCase):
    def setUp(self):
        rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        user = get_user_model().objects.create_user(
            username="Jojo",
            email="jojo@dio.com",
            password="itwasmedio",
        )
        self.client.login(username='Jojo', password='itwasmedio')
        i = 1
        while i <= 20:
            Ad.objects.create(action='O', title=f'foo{i}', description='donne cafe', image='ad/tests/1.jpg', city='Paris', user_id=user)
            Ad.objects.create(action='C', title=f'bar{i}', description='donne plante', image='ad/tests/1.jpg', city='Caen', user_id=user)
            i += 1
        self.response = self.client.get('/recherche/',
                                        {
                                            'query': 'annonce',
                                            'location': 'Paris'
                                        }
                                        )

    def tearDown(self):
        rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)
    
    def test_template(self):
        self.assertTemplateUsed('search.html')
    
    # test result with order
    def test_order(self):
        first = self.response.context['ad'][1]
        self.assertEqual(first, 'bar1')
    
    # test amount of result
    def test_count_ads(self):
        self.assertEqual(self.response.context['results'].count(), 20)

    # test which results come out
    def test_order(self):
        self.assertEqual(self.response.context['results'].first().title, 'bar1')
        self.assertEqual(self.response.context['results'].second().title, 'bar2')
        self.assertEqual(self.response.context['results'][21].title, 'foo1')

    # test city filter
    def test_city_filter(self):
        response = self.client.get('/rechercher/',
                                        {
                                            'query': 'annonce',
                                            'location': 'Caen'
                                        }
                                        )
        self.assertEqual(response.context['results'].first().title, 'donne plante1')
    