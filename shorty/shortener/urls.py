from django.conf.urls import url

from shortener.views import ShortLinkCreateView

urlpatterns = [
    url(r'^$', ShortLinkCreateView.as_view()),
]
