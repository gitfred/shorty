import random

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.crypto import get_random_string


class ShortLink(models.Model):
    """Represents shortened URL.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    link = models.CharField(max_length=50)
    destination = models.URLField()
    datetime_add = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('short-link-detail', kwargs={'link': self.link})

    @classmethod
    def find_free_link(cls, max_retries: int=10):
        """Looks for available link.

        :param max_retries: How many times method should try to find a free link
        :returns: link which can be used for createing new ShortLink
        :rtype: str
        :raises Exception: When free link couldn't be found

        """
        for _ in range(max_retries):
            # the length must have at most settings.SHORT_LINK_LEN chars
            link = get_random_string(random.randint(1, settings.SHORT_LINK_LEN))
            if not cls.objects.filter(link=link):
                return link

        raise Exception("Couldn't find link for {} retries".format(max_retries))
