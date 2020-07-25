`Para visualizar o README em português <https://github.com/rhenter/django-api-client/blob/master/README.pt.rst>`_.


=================
Django API Client
=================

|PyPI latest| |PyPI Version| |PyPI License|  |CicleCI Status| |Coverage| |Docs|

Django API Client is a client for APIs in general, which allows iterating with the API as if they were using a Local model in their project, through a client and Custom CBV (Class based Views)


Some reasons to use the **Django API Client**

* If you work with microservices with APIs in multiple locations and want to continue using Django as a WebApp with the same capabilities to render data as if you were using native models

* You want to separate your Django project to let one of them only with the API with DRF and the other as a WebApp with Templates (HTML), CSS, JS instead of using some JS frontend (ReactJS, AngularJS, etc.)

* You want to use a third party API to list, create and change using the django template system

For more information, see our documentation at `Read the Docs <http://django-api-client.readthedocs.io/en/latest/>`_.

Requirements
============

- Python 3.x
- Django 2.0 or later


How to install
==============

You can get Django Stuff by using pip:

.. code:: shell

    $ pip install django-api-client


If you want to install it from source, grab the git repository from Gitlab and run setup.py:

.. code:: shell

    $ git clone git@github.com:rhenter/django_api_client.git
    $ cd django_api_client
    $ python setup.py install


Config
======

To enable `django_api_client` in your project you need to add it to `INSTALLED_APPS` in your projects
`settings.py` file:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_api_client',
        ...
    )


Example
=======

- Adicione tambem ao settings.py a configuração para acessar sua API:

.. code-block:: python

    DJANGO_API_CLIENT = {
      'API': [
        {
            'NAME': 'production',
            'URL_BASE': 'https://example.com/v1',
            'ENDPOINTS': [
                '/order/orders',
                '/user/users',
                ...
            ],
            'AUTHENTICATION_ACCESS_TOKEN': 'TOKEN'
        },
        {
            'NAME': 'localhost',
            'URL_BASE': 'http://localhost:8001/v1',
            'ENDPOINTS': [
                '/order/orders',
                '/user/users',
                ...
            ],
            'AUTHENTICATION_ACCESS_TOKEN': 'TOKEN'
        }
      ]
    }


*Obs: Os detalhes de configuração serão explicados na documentação*

* Crie um arquivo clients.py em alguma pasta nucleo do seu projeto, caso não tenha crie dentro da sua pasta do projeto para ser simples de ser importado de qualquer lugar do projeto com o seguinte conteúdo:

.. code-block:: python

  from django_api_client.client import api_client_factory

  api_client = api_client_factory('production')


Obs:
  - O nome desta variável será o nome nome do cliente que você usará em todo o seu projeto
  - Recomendo para produção usar uma env var setada no settings.py para você poder alterar de maneira simples o nome da API sem a necessidade de criar varios.
  - No nosso caso, temos a opção de "production" e "localhost", o factory gerará o cliente de acordo com o nome utilizado e os parametros descritos nele

* Agora vamos listar os dados usando o sistema de templates normal do Django

Vamos imaginar que o cliente esta na pasta de projeto (pasta que contem o arquivo settings.py)

.. code-block:: python

  from django_api_client.mixins import ClientAPIListMixin

  from pasta_do_projeto.clients import api_client


  class OrderListView(ClientAPIListMixin):
      template_name = "template_name.html"        # Caminho do seu template HTML
      page_title = 'Orders'                       # Gera uma variavel de contexto para usar no seu template
      page_base_url = reverse_lazy('order:list')  # Informação usada na paginação
      paginate_by = 50                            # Número de items para gerar a paginação
      client_method = api_client.order.get_orders


Obs:
  O cliente gerará para cada endpoint a toda uma estrutura amigavel para o usuário. Exemplo com o endpoint */order/orders/*:

.. code-block:: text

    nome do endpoint: order
    métodos:
        get_orders   # GET: Listar
        get_order    # GET: Detalhe de um recurso usando um identificador
        create_order # POST: Cria um registro de um recurso
        update_order # PUT/PATCH: Atualiza total ou parciamente um recurso usando um identificador
  O que isso quer dizer?
    Que o cliente sempre gerará a estutura de acordo os nomes dos seus endpoints

Documentation
=============

Check out the latest ``django-api-client`` documentation at `Read the Docs <http://django-api-client.readthedocs.io/en/latest/>`_


Contributing
============

Please send pull requests, very much appreciated.


1. Fork the `repository <https://github.com/rhenter/django_api_client>`_ on GitHub.
2. Make a branch off of master and commit your changes to it.
3. Install requirements. ``pip install -r requirements-dev.txt``
4. Install pre-commit. ``pre-commit install``
5. Run the tests with ``cd test-django-project; py.test -vv -s``
6. Create a Pull Request with your contribution


.. |Docs| image:: https://readthedocs.org/projects/django-api-client/badge/?version=latest
   :target: http://django-api-client.readthedocs.org/en/latest/?badge=latest
.. |PyPI Version| image:: https://img.shields.io/pypi/pyversions/django-api-client.svg?maxAge=60
   :target: https://pypi.python.org/pypi/django-api-client
.. |PyPI License| image:: https://img.shields.io/pypi/l/django-api-client.svg?maxAge=120
   :target: https://github.com/rhenter/django-api-client/blob/master/LICENSE
.. |PyPI latest| image:: https://img.shields.io/pypi/v/django-api-client.svg?maxAge=120
   :target: https://pypi.python.org/pypi/django-api-client
.. |CicleCI Status| image:: https://circleci.com/gh/rhenter/django-api-client.svg?style=svg
   :target: https://circleci.com/gh/rhenter/django-api-client
.. |Coverage| image:: https://codecov.io/gh/rhenter/django-api-client/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/rhenter/django-api-client
