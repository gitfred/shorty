from django.conf import settings
from django.contrib.auth import get_user_model
import requests

User = get_user_model()


def generate_random_users(number):

