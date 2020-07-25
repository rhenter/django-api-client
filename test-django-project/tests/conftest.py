from unittest import mock

import pytest

from django_api_client.client import api_client_factory, BaseAPI


@pytest.fixture
def api_client():
    return api_client_factory('localhost')


@pytest.fixture
def fake_client():
    access_token = 'fake-token'

    class FakeClient(BaseAPI):
        base_urls = {
            "practice": "http://example.com",
        }

    return FakeClient(environment="practice", access_token=access_token)


@pytest.fixture
def fake_session():
    get = mock.Mock(return_value=mock.Mock(status_code=200))
    post = mock.Mock(return_value=mock.Mock(status_code=201))
    delete = mock.Mock(return_value=mock.Mock(status_code=204))
    patch = mock.Mock(return_value=mock.Mock(status_code=200))
    put = mock.Mock(return_value=mock.Mock(status_code=200))

    return mock.Mock(
        get=get, post=post, put=put, patch=patch, delete=delete, headers={}
    )
