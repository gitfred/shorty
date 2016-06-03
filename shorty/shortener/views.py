import logging

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, RedirectView

from shortener.models import ShortLink

logger = logging.getLogger(__name__)

User = get_user_model()


class ShortLinkCreateView(CreateView):
    """Create ShortLink view.

    Creates ShortLink or redirects to existing one.
    """
    model = ShortLink
    fields = ['destination']

    def form_valid(self, form):
        """Create new ShortLink with random user.

        Receives ShortLink create form, assigns random user
        as its owner and generates short link for its desination.
        If the ShortLink with the desination already exists, user is
        redirected to the existing one immediately.

        :param form: a ModelForm object
        :returns: HttpRedirect to desination url
        """
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
    """ShortLink detail view

    Simply returns basic information about ShortLink such as author,
    short link and destination URL. It uses 'link' model field instead of 'pk'.
    """
    model = ShortLink

    def get_object(self, queryset=None):
        queryset = queryset or self.get_queryset()
        return get_object_or_404(queryset, link=self.kwargs['link'])


class ShortLinkRedirectView(RedirectView):
    """ShortLink redirect view

    Redirects user to the destination URL based on 'link'.
    """

    def get_redirect_url(self, *args, **kwargs):
        short_link = get_object_or_404(ShortLink, link=kwargs['link'])
        return short_link.destination
