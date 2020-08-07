=================
Django API Client
=================

|PyPI latest| |PyPI Version| |PyPI License|  |CicleCI Status| |Coverage| |Docs| |Open Source? Yes!|

O Django API Client é um wrapper de resposta da API, que traduz as chamadas nativas do Django ao usar uma view para a uma determinada API REST. Seja usando do cliente da API diretamente em um FBV (Function-based View) ou usando CBV (Class-based View), essa biblioteca tornar essa comunicação o mais transparente e fácil o possível


Alguns motivos para se usar o **Django API Client**

* Se você trabalha com microsserviços com APIs em vários locais e deseja continuar usando o Django como um WebApp com os mesmos recursos para renderizar os dados como se estivesse usando os modelos nativos

* Você quer separar o seu projeto Django para deixar um deles somente com a API com DRF e outro como um WebApp com Templates(HTML), CSS, JS ao invés de usar algum frontend JS (ReactJS, AngularJS, etc)

* Você deseja usar uma API de terceiros para listar, criar e alterar usando o sistema de templates do django


Para mais informações, veja nossa documentação em `Github Pages <https://rhenter.github.io/django-api-client/>`_

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
            'BASE_URL': 'https://example.com',
            'ENDPOINTS': [
                '/v1/order/orders',
                '/v1/user/users',
                ...
            ],
            'AUTHENTICATION_ACCESS_TOKEN': 'TOKEN'
        },
        {
            'NAME': 'localhost',
            'BASE_URL': 'http://localhost:8001',
            'ENDPOINTS': [
                '/v1/order/orders',
                '/v1/user/users',
                ...
            ],
            'AUTHENTICATION_ACCESS_TOKEN': 'TOKEN'
        }
      ]
    }

.. note::
  Os detalhes de configuração serão explicados na documentação*

* Crie um arquivo clients.py em alguma pasta nucleo do seu projeto, caso não tenha, crie dentro da sua pasta do projeto para ficar mais simples de ser importado de qualquer lugar do projeto com o seguinte conteúdo:

.. code-block:: python

  from django_api_client.client import api_client_factory

  api_client = api_client_factory('production')


.. note::
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
      page_base_url = reverse_lazy('order:list')  # Informação usada na paginação e na busca
      paginate_by = 50                            # Número de items para gerar a paginação
      client_method = api_client.order.orders.list


.. note::
  O cliente gerará para cada endpoint a toda uma estrutura amigável para o usuário.


No seu template você pode usar os includes (snippets) de formularios e paginação. Ex:


.. code-block:: jinja

    {% content %}

    ...
    <div class="card card-navy card-outline">
      <div class="card-header">
        <h3 class="card-title">
          {% trans "Order List" %} : <small class="text-muted">{{ paginator.count }}</small>
        </h3>
        {% include "includes/form_paginate_by.html" with paginate_by=paginate_by range_pagination=range_pagination %}
        {% include "includes/form_search.html" with search=search %}
      </div>
      <div class="card-body table-responsive p-0">
        <table class="table table-bordered table-hover table-striped" id="list-content">
          <thead>
          <tr>
            <th>{% trans 'Code' %}</th>
            <th>{% trans 'Customer' %}</th>
            <th>{% trans 'Product' %}</th>
          </tr>
          </thead>
          <tbody class="text-gray">
          {% for order in object_list %}
            <tr>
              <td><a href="{% url 'order:detail' pk=order.id %}" </a>
              </td>
              <td>{{ order.id }}</td>
              <td>{{ order.customer.name|title }}</td>
              <td>{{ order.product.name|title }}</td>
            </tr>
            {% endfor %}
          {% endif %}
          </tbody>
        </table>
      </div>
      <div class="card-footer">
        {% if object_list|length != 0 or not object_list %}
          {% include "includes/list_paginator.html" with page_obj=page_obj paginator=paginator %}
        {% endif %}
      </div>
    </div>


.. note::
  - Exemplo using estilos (styles) do Bootstrap
  - includes/form_search.html: Form com input de busca. Este include suporta placeholder também.
  - includes/form_paginate_by.html: Form com select para escolher por quantos elementos a pagina será paginada. Ex: (20, 40, 60, etc ...)
  - includes/list_paginator.html: Bloco com os elementos de paginação com os botões dos número de paginas, anterior e próximo



Exemplo com o endpoint **/order/orders/**:

.. code-block:: text

    nome do endpoint: order
    métodos:
        get_orders   # GET: Listar
        get_order    # GET: Detalhe de um recurso usando um identificador
        create_order # POST: Cria um registro de um recurso
        update_order # PUT/PATCH: Atualiza total ou parciamente um recurso usando um identificador

.. hint::

    O que isso quer dizer?
      Que o API Cliente sempre gerará a estutura de acordo os nomes dos seus endpoints

Documentação
============

Verifique a ultima versão da documentação do ``django-api-client`` em `Github Pages <https://rhenter.github.io/django-api-client/>`_


Quer contribuir?
================

Por favor envie seus Pull Requests, eles serão muito apreciados.


1. Faça o Fork do `repositorio <https://github.com/rhenter/django_api_client>`_ no GitHub.
2. Crie uma branch fora da master e commit suas alterações.
3. Instale os dependências. ``pip install -r requirements-dev.txt``
4. Instale o pre-commit. ``pre-commit install``
5. Rode os tests com ``cd test-django-project; py.test -vv -s``
6. Crie um Pull Request com a sua contribuição


.. |Docs| image:: https://img.shields.io/static/v1?label=DOC&message=GitHub%20Pages&color=%3CCOLOR%3E
   :target: https://rhenter.github.io/django-api-client/
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
.. |Open Source? Yes!| image:: https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github
   :target: https://github.com/rhenter/django-api-client