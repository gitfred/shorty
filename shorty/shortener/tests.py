from django.contrib.auth import get_user_model
from django.test import Client
from django.test import TestCase

from shortener.models import ShortLink

User = get_user_model()


class TestShortLinkViews(TestCase):

    def setUp(self):
        self.client = Client()

    def create_user(self, username='sylwek'):
        return User.objects.create(username=username)

    def test_create_and_redirect(self):
        self.create_user()
        url = 'http://httpbin.org/'
        resp = self.client.post('/', {'destination': url})

        link = ShortLink.objects.last()

        self.assertRedirects(resp, link.get_absolute_url())
        self.assertEqual(link.destination, url)

        # try once again
        resp = self.client.post('/', {'destination': url})
        link = ShortLink.objects.last()

        # should be still 1
        self.assertEqual(ShortLink.objects.count(), 1)

    def test_redirect(self):
        link = ShortLink.objects.create(
            user=self.create_user(),
            link='QQQ',
            destination='http://example.com/',
        )
        resp = self.client.get('/QQQ')

        self.assertRedirects(resp, link.destination)
