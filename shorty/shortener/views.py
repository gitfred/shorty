import logging

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, RedirectView

from shortener.models import ShortLink

logger = logging.getLogger(__name__)

User = get_user_model()


class ShortLinkCreateView(CreateView):
    model = ShortLink
    fields = ['destination']

    def form_valid(self, form):
        short_link = form.save(commit=False)
        # get random user
        short_link.user = User.objects.order_by('?').first()

        duplicates = self.model.objects.filter(
            destination=short_link.destination)
        if duplicates:
            duplicate = duplicates.first()
            logger.info("Found duplicate of %s (%s)",
                        duplicate.destination, duplicate.link)
            return redirect(duplicate)

        short_link.link = self.model.find_free_link()
        return super().form_valid(form)


class ShortLinkDetailView(DetailView):
    model = ShortLink

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, link=self.kwargs['link'])


class ShortLinkRedirectView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        short_link = get_object_or_404(ShortLink, link=kwargs['link'])
        return short_link.destination
