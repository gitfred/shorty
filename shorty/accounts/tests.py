from django.contrib.auth import get_user_model
from django.test import TestCase
import requests_mock

from accounts import utils

User = get_user_model()


class TestUtils(TestCase):

    @requests_mock.Mocker()
    def test_generate_rangom_users(self, mrequests):
        response_json = {
            'info': {
                'page': 1,
                'results': 1,
                'seed': '7a4f3b4bee464743',
                'version': '1.0'
            },
            'results': [
                {
                    'email': 'dawn.castro@example.com',
                    'login': {
                        'md5': 'c87d5a87e533d4f2aa6073a599377a82',
                        'password': 'bathing',
                        'salt': 'nan',
                        'sha1': 'nan',
                        'sha256': 'nan',
                        'username': 'beautifulgoose142'},
            'name': {'first': 'dawn', 'last': 'castro', 'title': 'mrs'},
            'registered': 1385178139},
            ]
        }

        resp = mrequests.get(requests_mock.ANY, json=response_json)

        utils.generate_random_users(1)

        self.assertEqual(resp.call_count, 1)
        self.assertEqual(User.objects.count(), 1)

        user = User.objects.first()

        data = response_json['results'][0]
        self.assertEqual(user.first_name, data['name']['first'])
        self.assertEqual(user.last_name, data['name']['last'])
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.date_joined.timestamp(), data['registered'])
