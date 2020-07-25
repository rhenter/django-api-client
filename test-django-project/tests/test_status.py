from django_api_client import status


def test_is_informational():
    assert status.is_informational(105)


def test_is_success():
    assert status.is_success(202)


def test_is_redirect():
    assert status.is_redirect(304)


def test_is_client_error():
    assert status.is_client_error(403)


def test_is_server_error():
    assert status.is_server_error(500)


def test_200_ok():
    assert status.HTTP_200_OK == 200


# Dummy tests.
def test_all():
    for k, v in vars(status).items():
        assert vars(status).get(k) == v
