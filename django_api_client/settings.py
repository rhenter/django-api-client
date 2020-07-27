"""
Settings for API Client are all namespaced in the DJANGO_API_CLIENT setting.
For example your project's `settings.py` file might look like this:

DJANGO_API_CLIENT = {
    'API': {
        'NAME': 'API NAME',
        'BASE_URL': 'https://example.com/v1',
        'ENDPOINTS': [
            '/order/orders',
            '/user/users',
            ...
        ],
        'AUTHENTICATION_ACCESS_TOKEN': 'header' or 'url'
        'AUTHENTICATION_ACCESS_TOKEN_TYPE': 'Bearer', 'Token', ...
    },
}

This module provides the `api_client_setting` object, that is used to access
Django API Client settings, checking for user settings first, then falling
back to the defaults.
"""
from django.conf import settings
from django.test.signals import setting_changed

DEFAULT_SETTINGS_KEY = 'DJANGO_API_CLIENT'
API_DEFAULTS = {
    'AUTHENTICATION_ACCESS_TOKEN': None,
    'AUTHENTICATION_ACCESS_TOKEN_TYPE': 'Bearer',
    'AUTHENTICATION_METHOD': 'header',
    'AUTHENTICATION_URL_EXTRA_PARAMS': [],
    'AUTHENTICATION_URL_KEY': 'token',
    'BASE_URL': None,
    'ENDPOINTS': [],
    'LOCALE': getattr(settings, 'LANGUAGE_CODE', 'en'),
    'NAME': None,
    'URL_APPEND_SLASH': True,
    'TIMEOUT': 3,
}
DEFAULTS = {
    'PAGE_SIZE': 100,
    'SLUG_FIELD': 'id'
}
REQUIRED_KEYS = ['NAME', 'BASE_URL', 'ENDPOINTS']


class APIClientSettings:
    """
    A settings object that allows Django API Client settings to be accessed as
    properties. For example:

        from django_api_client.settings import api_client_settings
        print(api_client_settings.API)

    Any setting with string import paths will be automatically resolved
    and return the class, rather than the string literal.
    """

    def __init__(self, user_settings=None, defaults=None, api_defaults=None):
        if user_settings:
            self._user_settings = user_settings
        self.api_defaults = api_defaults or API_DEFAULTS
        self.defaults = defaults or DEFAULTS
        self._cached_attrs = set()
        self.apis = self._set_apis()
        self.configs = self._get_defaults_configs()

    def _get_api_configs(self, api_settings):
        configs = {}

        for req_attr in REQUIRED_KEYS:
            if req_attr not in api_settings:
                raise AttributeError(f"Key Required: '{req_attr}'")

        for user_attr in api_settings:
            if user_attr not in self.api_defaults:
                raise AttributeError(f"Invalid API setting: '{user_attr}'")

        for attr in self.api_defaults:
            try:
                # Check if present in user settings
                val = api_settings[attr]
            except KeyError:
                # Fall back to defaults
                val = self.api_defaults[attr]

            if attr == 'BASE_URL' and not val.startswith('http'):
                raise AttributeError(f"Invalid Base URL: '{val}'. Please add a URL with http or https as prefix.")

            configs[attr] = val
            # Cache the result
            self._cached_attrs.add(attr)
        return configs

    def _get_defaults_configs(self):
        configs = {}

        for user_attr in self.user_settings:
            if user_attr != 'API' and user_attr not in self.defaults:
                raise AttributeError(f"Invalid Global Setting: '{user_attr}'")

        for attr in self.defaults:
            try:
                # Check if present in user settings
                val = self.user_settings[attr]
            except KeyError:
                # Fall back to defaults
                val = self.defaults[attr]

            configs[attr] = val
            # Cache the result
            self._cached_attrs.add(attr)
        return configs

    def _set_apis(self):
        api_settings = self.user_settings.get('API', '')
        if not api_settings:
            return

        apis = []
        if isinstance(api_settings, dict):
            apis.append(self._get_api_configs(api_settings))
        elif isinstance(self.user_settings, list):
            for api in api_settings:
                apis.append(self._get_api_configs(api))
        return apis

    @property
    def api_names(self):
        return [api['NAME'] for api in self.apis]

    @property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(settings, DEFAULT_SETTINGS_KEY, {})
        return self._user_settings

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()
        if hasattr(self, '_user_settings'):
            delattr(self, '_user_settings')

    def __repr__(self):
        return '<APIClientSettings>'

    def __str__(self):
        names = ' '.join([name.title() for name in self.api_names])
        return f'APIClientSettings: {names}'


api_client_settings = APIClientSettings(None, DEFAULTS)


def reload_api_settings(*args, **kwargs):
    setting = kwargs['setting']
    if setting == DEFAULT_SETTINGS_KEY:
        api_client_settings.reload()


setting_changed.connect(reload_api_settings)
