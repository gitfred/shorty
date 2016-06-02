from django.views.generic import CreateView

from shortener.models import ShortLink


class ShortLinkCreateView(CreateView):
    model = ShortLink
    fields = ['link', 'destination']
