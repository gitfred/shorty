from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.crypto import get_random_string


class ShortLink(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    link = models.CharField(max_length=50)
    destination = models.URLField()
    datetime_add = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('short-link-detail', kwargs={'link': self.link})

    @classmethod
    def find_free_link(cls, max_retries=10):
        for _ in range(max_retries):
            link = get_random_string(settings.SHORT_LINK_LEN)
            if not cls.objects.filter(link=link):
                return link

        raise Exception("Couldn't find link for {} reties".format(max_retries))
