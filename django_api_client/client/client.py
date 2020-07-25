from django.utils.translation import gettext_lazy as _

from django_api_client.settings import api_client_settings, DEFAULTS
from .base import BaseAPI, BaseEndpoint
from .exceptions import APINotFound


class APIClient:
    """API Client Factory Class
    This class instantiates all endpoint classes
    """

    def __init__(self, **kwargs):
        """API object to communicate with API.
        """
        self.api = BaseAPI(**kwargs)
        for endpoint_url in kwargs['endpoints']:
            endpoint = BaseEndpoint(api=self.api, endpoint=endpoint_url)
            setattr(self, endpoint.endpoint_name, endpoint)

    def __repr__(self):
        return f'<APIClient {self.api.api_name.title()}>'


def api_client_factory(api_name=''):
    if not api_name:
        raise AttributeError(_('API name is required.'))
    api_configs = next((api for api in api_client_settings.apis if api['NAME'] == api_name), None)
    if not api_configs:
        raise APINotFound(_('API name Not Found.'))

    api_args = {
        'api_name': api_configs.get('NAME', DEFAULTS['NAME']),
        'base_url': api_configs.get('BASE_URL', DEFAULTS['BASE_URL']),
        'access_token': api_configs.get('AUTHENTICATION_ACCESS_TOKEN', DEFAULTS['AUTHENTICATION_ACCESS_TOKEN']),
        'access_token_type': api_configs.get(
            'AUTHENTICATION_ACCESS_TOKEN_TYPE', DEFAULTS['AUTHENTICATION_ACCESS_TOKEN_TYPE']),
        'authentication_method': api_configs.get('AUTHENTICATION_METHOD', DEFAULTS['AUTHENTICATION_METHOD']),
        'authentication_url_extra_params': api_configs.get(
            'AUTHENTICATION_URL_EXTRA_PARAMS', DEFAULTS['AUTHENTICATION_URL_EXTRA_PARAMS']),
        'authentication_url_key': api_configs.get('AUTHENTICATION_URL_KEY', DEFAULTS['AUTHENTICATION_URL_KEY']),
        'endpoints': api_configs.get('ENDPOINTS', DEFAULTS['ENDPOINTS']),
        'locale': api_configs.get('LOCALE', DEFAULTS['LOCALE']),
        'url_append_slash': api_configs.get('URL_APPEND_SLASH', DEFAULTS['URL_APPEND_SLASH']),
        'timeout': api_configs.get('TIMEOUT', DEFAULTS['TIMEOUT']),
    }
    return APIClient(**api_args)
