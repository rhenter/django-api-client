import pytest

from django_api_client.client.factories import ResponseFactory


def test_response_factory():
    data = {'users': [{'id': '000-000-0000000-000', 'tags': []}]}

    class ResponseTest:
        def json(self):
            return data

    user_id = data['users'][0]['id']
    response = ResponseFactory(ResponseTest(), 'data/test')
    assert response.as_dict() == data

    obj = response.as_obj()
    assert obj.users[0].id == user_id


@pytest.mark.parametrize('endpoint,expected', [
    ('data/test', 'DataTest'),
    ('base/target/DETAIL', 'BaseTarget'),
    ('base/sub/123123', 'BaseSub'),
    ('test/data', 'TestData'),
])
def test_factory_str(endpoint, expected):
    data = {'users': [{'id': '000-000-0000000-000', 'tags': []}]}

    class ResponseTest:
        def json(self):
            return data

    factory = ResponseFactory(ResponseTest(), endpoint)

    assert str(factory) == expected


@pytest.mark.parametrize('endpoint,expected', [
    ('data/test', 'DataTest'),
    ('base/target/DETAIL', 'BaseTarget'),
    ('base/sub/123123', 'BaseSub'),
    ('test/data', 'TestData'),
])
def test_factory_repr(endpoint, expected):
    data = {'users': [{'id': '000-000-0000000-000', 'tags': []}]}

    class ResponseTest:
        def json(self):
            return data

    factory = ResponseFactory(ResponseTest(), endpoint)

    assert repr(factory) == f'<APIClient {expected} object>'
