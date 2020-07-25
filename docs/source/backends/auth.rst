EmailOrUsernameModelBackend
---------------------------

Backend to login using email or username.

Usage:

Add before the default ModelBackend

.. code-block:: python

    AUTHENTICATION_BACKENDS = (
        'django_api_client.backends.auth.EmailOrUsernameModelBackend',
        'django.contrib.auth.backends.ModelBackend'
    )

