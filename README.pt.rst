=================
Django API Client
=================

|PyPI latest| |PyPI Version| |PyPI License|  |CicleCI Status| |Coverage| |Docs|

Django API Client é um cliente para APIs em geral, que possibilita iteragir com a API como se tivessem usando um modelo Local no seu projeto, atravês de um client e CBV (Class based Views) Customizadas


Alguns motivos para se usar o **Django API Client**

* Se você trabalha com microsserviços com APIs em vários locais e deseja continuar usando o Django como um WebApp com os mesmos recursos para renderizar os dados como se estivesse usando os modelos nativos

* Você quer separar o seu projeto Django para deixar um deles somente com a API com DRF e outro como um WebApp com Templates(HTML), CSS, JS ao invés de usar algum frontend JS (ReactJS, AngularJS, etc)

* Você deseja usar uma API de terceiros para listar, criar e alterar usando o sistema de templates do django


Para mais informações, veja nossa documentação em `Read the Docs <http://django-api-client.readthedocs.io/en/latest/>`_.

Ref:
`* Queryset: (Resultado de uma busca usando o ORM do Django)`

Dependências
============

- Python 3.x
- Django 2.0 or later


Como instalar
=============

Você pode instalar usando **pip**:

.. code:: shell

    $ pip install django-api-client

Se preferir, você pode baixar o codigo no Repositório do GitHub e rodar o setup.py

.. code:: shell

    $ git clone git@github.com:rhenter/django_api_client.git
    $ cd django_api_client
    $ python setup.py install


Configurando
============

Para habilitar o `django_api_client` você precisa adiciona-lo ao `INSTALLED_APPS` no arquivo settings.py do seu projeto:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_api_client',
        ...
    )


Exemplo
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
  O cliente gerará para cada endpoint a toda uma estrutura amigavel para o usuário.


Exemplo com o endpoint **/order/orders/**:

.. code-block:: text

    nome do endpoint: order
    métodos:
        get_orders   # GET: Listar
        get_order    # GET: Detalhe de um recurso usando um identificador
        create_order # POST: Cria um registro de um recurso
        update_order # PUT/PATCH: Atualiza total ou parciamente um recurso usando um identificador
  O que isso quer dizer?
    Que o cliente sempre gerará a estutura de acordo os nomes dos seus endpoints

Documentação
============

Verifique a ultima versão da documentação do ``django-api-client`` em `Read the Docs <http://django-api-client.readthedocs.io/en/latest/>`_


Quer contribuir?
================

Por favor envie seus Pull Requests, eles serão muito apreciados.


1. Faça o Fork do `repositorio <https://github.com/rhenter/django_api_client>`_ no GitHub.
2. Crie uma branch fora da master e commit suas alterações.
3. Instale os dependências. ``pip install -r requirements-dev.txt``
4. Instale o pre-commit. ``pre-commit install``
5. Rode os tests com ``cd test-django-project; py.test -vv -s``
6. Crie um Pull Request com a sua contribuição


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
