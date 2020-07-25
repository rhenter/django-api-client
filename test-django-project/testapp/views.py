from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, TemplateView

from apps.core.mixins import BaseViewMixin, ClientAPIDetailMixin, ClientAPIListMixin

from test_django_project.clients import api_client

from .forms import CreditCardForm

SESSION_NAME = 'giftcard-company'


class GiftCardsListView(ClientAPIListMixin):
    template_name = "giftcard/giftcard_list.html"
    page_title = _('Gift Cards')
    page_base_url = reverse_lazy('giftcard:list')
    paginate_by = 50
    client_method = api_client.giftcard.get_giftcards
    extra_kwargs = ['featured']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        featureds = api_client.giftcard.get_giftcards(params={'featured': True})
        context['featureds'] = featureds.as_obj().results
        return context


class DetailsGiftCardView(BaseViewMixin, FormView):
    form_class = CreditCardForm
    template_name = "giftcard/giftcard_details.html"
    page_title = _('Gift Cards Details')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        giftcard = api_client.giftcard.get_giftcard(code=self.kwargs.get('code'))
        context['object'] = giftcard.as_dict()
        return context


class ConfirmedGiftCardView(ClientAPIDetailMixin):
    template_name = "giftcard/giftcard_confirmed.html"
    page_title = _('Gift Cards - Confirmed')
    client_method = api_client.giftcard.get_giftcard


# class DiscountsTestView(BaseLis