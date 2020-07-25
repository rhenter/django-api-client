from django.urls import reverse_lazy

from django_api_client.views import ClientAPIDetailView, ClientAPIListView
from test_django_project.clients import api_client


class TestClientAPIListView(ClientAPIListView):
    template_name = "view.html"
    page_base_url = reverse_lazy('test:list')
    paginate_by = 50
    client_method = api_client.giftcard.get_giftcards


class TestClientAPIDetailView(ClientAPIDetailView):
    template_name = "view.html"
    client_method = api_client.giftcard.get_giftcard
