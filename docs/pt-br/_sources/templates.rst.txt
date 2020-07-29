Templates
=========

In your template you can use the forms and pagination snippets. E.g:


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
  - Example using Bootstrap Styles(CSS)
  - includes/form_search.html: Form with search input. This ``include`` support placeholder too.
  - includes/form_paginate_by.html: Select form to choose how many elements the page will be paginate. Ex: by (20, 40, 60, etc ...)
  - includes/list_paginator.html: Block with pagination elements with the number of pages buttons, previous and next

