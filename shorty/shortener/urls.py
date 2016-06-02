from django.conf.urls import url

from shortener.views import (
    ShortLinkCreateView,
    ShortLinkDetailView,
    ShortLinkRedirectView,
)

urlpatterns = [
    url(r'^$', ShortLinkCreateView.as_view()),
    url(r'^!(?P<link>\w+)/?$', ShortLinkDetailView.as_view(),
        name='short-link-detail'),

    # should be the last on the list since catches everything
    url(r'^(?P<link>\w+)/?$', ShortLinkRedirectView.as_view()),
]
