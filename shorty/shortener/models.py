from django.db import models
from django.conf import settings


class ShortLink(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    link = models.CharField(max_length=50)
    destination = models.URLField()
    datetime_add = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
