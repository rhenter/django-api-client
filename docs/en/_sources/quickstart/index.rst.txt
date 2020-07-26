Requirements
============

- Python 3.x
- Django 2.0 or later


How to install
==============

You can get Django API Client by using pip:

.. code:: shell

    $ pip install django-api-client


If you want to install it from source, grab the git repository from GitHub and run setup.py:

.. code:: shell

    $ git clone git@github.com:rhenter/django_api_client.git
    $ cd django_api_client
    $ python setup.py install


How to Config
=============

To enable `django_api_client` in your project you need to add it to `INSTALLED_APPS` in your projects
`settings.py` file:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_api_client',
        ...
    )
