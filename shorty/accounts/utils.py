import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
import requests

User = get_user_model()

logger = logging.getLogger(__name__)


def generate_random_users(number: int):
    """Function for generating fake random users.

    :param number: number of users to be created
    """
    resp = requests.get(
        settings.RANDOMUSER_ME_URL,
        params={
            'results': number,
            'inc': 'name,login,registered,email',
        }
    )
    resp.raise_for_status()
    fake_users = resp.json()

    users_list = []
    for user in fake_users['results']:
        date_joined = timezone.make_aware(
            timezone.datetime.fromtimestamp(user['registered'])
        )

        user_obj = User(
            username=user['login']['username'],
            first_name=user['name']['first'],
            last_name=user['name']['last'],
            email=user['email'],
            password=user['login']['password'],
            date_joined=date_joined,
        )
        users_list.append(user_obj)
        logger.debug('New fake user data fetched: %s %s', user_obj.first_name,
                     user_obj.last_name)

    User.objects.bulk_create(users_list)
