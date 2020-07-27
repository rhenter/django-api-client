Django API Client Documentation
===============================

The Django API Client is an API response wrapper, which allows you to iterate through the API as if they were using a local model / object in your project. Whether through the direct customer in an FBV or using personalized CBV (class-based displays), this framework tries to make this communication as easy as possible


Some reasons to use the **Django API Client**

* If you work with microservices with APIs in multiple locations and want to continue using Django as a WebApp with the same capabilities to render data as if you were using native models

* You want to separate your Django project to let one of them only with the API with DRF and the other as a WebApp with Templates (HTML), CSS, JS instead of using some JS frontend (ReactJS, AngularJS, etc.)

* You want to use a third party API to list, create and change using the django template system


Quickstart
==========

.. toctree::
    :maxdepth: 2

    quickstart/index.rst


User Guide
==========

.. toctree::
    :maxdepth: 2
    :numbered:

    client/index.rst
    forms/index.rst
    views/index.rst
    templates.rst
    example.rst


Development
===========

.. toctree::
    :maxdepth: 2
    :numbered:

    development/installation.rst
    development/documentation.rst
    development/release.rst


Downloads
=========

- `PDF <https://readthedocs.org/projects/django-api-client/downloads/pdf/latest/>`_

- `Epub <https://readthedocs.org/projects/django-api-client/downloads/epub/latest/>`_


Changelog
=========

.. toctree::

    changelog.rst
