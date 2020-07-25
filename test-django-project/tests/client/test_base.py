import json
from unittest.mock import Mock

import pytest
from requests.exceptions import ConnectionError as RequestsConnectionError, ReadTimeout, Timeout

from django_api_client.client.exceptions import NotFound, ServerError
from ..vcr import vcr


@pytest.fixture
def url_base():
    return 'http://localhost:8001/v1/'


@pytest.fixture
def endpoint():
    return 'fake/endpoint/'


@vcr.use_cassette()
def test_sync_with_endpoint_not_fount(api_client, endpoint):
    with pytest.raises(NotFound) as error:
        api_client.api.search(endpoint)

    assert str(error.value) == 'API server returned [404] status code, with message: (Endpoint Not Found)'


def test_sync_with_server_error(api_client, endpoint):
    api_client.api.make_request = Mock(side_effect=ServerError('foo'))

    with pytest.raises(ServerError) as error:
        api_client.api.search(endpoint)

    assert str(error.value) == 'API server returned a internal server error'


@pytest.mark.parametrize('exception', [
    Timeout, ReadTimeout, RequestsConnectionError,
])
def test_sync_with_requests_error(api_client, endpoint, exception):
    api_client.api.transport.make_request = Mock(side_effect=exception('foo'))

    with pytest.raises(ServerError) as error:
        api_client.api.search(endpoint)

    assert str(error.value) == 'API server returned a internal server error'


def test_sync_search(api_client, fake_session, endpoint, url_base):
    api_client.api.transport.session = fake_session
    api_client.api.search(endpoint)
    assert fake_session.get.called
    assert fake_session.get.call_args[0][0] == url_base + endpoint
    assert fake_session.get.call_args[1]['params'] == {}


def test_sync_search_with_params(
        api_client,
        fake_session,
        endpoint,
        url_base):
    api_client.api.transport.session = fake_session
    api_client.api.search(endpoint, params={'status': 'open'})
    assert fake_session.get.called
    assert fake_session.get.call_args[0][0] == url_base + endpoint
    assert fake_session.get.call_args[1]['params'] == {'status': 'open'}


def test_sync_create(api_client, fake_session, endpoint, url_base):
    api_client.api.transport.session = fake_session
    payload = {
        "order": {
            "units": "100",
            "instrument": "EUR_USD",
            "timeInForce": "FOK",
            "type": "MARKET",
            "positionFill": "DEFAULT"
        }
    }
    api_client.api.create(endpoint, data=payload)
    assert fake_session.post.called
    assert fake_session.post.call_args[0][0] == url_base + endpoint
    assert fake_session.post.call_args[1]['data'] == json.dumps(payload)


def test_sync_update_with_put(api_client, fake_session, endpoint, url_base):
    api_client.api.transport.session = fake_session
    payload = {
        "order": {
            "timeInForce": "GTC",
            "price": "1.7000",
            "type": "TAKE_PROFIT",
            "tradeID": "6368"
        }
    }
    api_client.api.update(endpoint + '6368', data=payload)
    assert fake_session.put.called
    assert fake_session.put.call_args[0][0] == url_base + endpoint + '6368/'
    assert fake_session.put.call_args[1]['data'] == json.dumps(payload)


def test_sync_update_with_patch(api_client, fake_session, endpoint, url_base):
    api_client.api.transport.session = fake_session
    payload = {'instrument': 'EUR_USD'}
    api_client.api.update(endpoint + '1234', data=payload, partial=True)
    assert fake_session.patch.called
    assert fake_session.patch.call_args[0][0] == url_base + endpoint + '1234/'
    assert fake_session.patch.call_args[1]['data'] == json.dumps(payload)
