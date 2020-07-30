Dynamic Form and Field
======================

DynamicForm
-----------

In the same way that ModelForm does not need to manually add each attribute, using DynamicForm, you just need to add the field name with an additional one that allows you to add the "Label Name" to the list


- Simple Example

.. code-block:: python

  from django_api_client.forms import DynamicForm

  ...


  class CompanyExampleForm(DynamicForm):

      class Meta:
          dynamic_fields = {
              'name',
              'brand',
              'cnpj',
          }


- Advanced Example with custom fields and ``label`` name


.. code-block:: python

  from django_api_client.forms import DynamicForm

  ...

  class CompanyExampleForm(DynamicForm):
      phone = forms.CharField(max_length=15, label=_('Phone'))
      cellphone = forms.CharField(max_length=20, label=_('Cellphone'))
      email_contact = forms.EmailField(label=_('Contact Email'))
      active = forms.BooleanField()

      class Meta:
          dynamic_fields = {
              'name': _("Company Name"),
              'brand': _("Brand"),
              'cnpj': _("CNPJ"),
              'phone': '',
              'cellphone': '',
              'email_contact': '',
              'active': '',
          }


- Advanced Example with validation


.. code-block:: python


  from django_api_client.forms import DynamicForm

  # These imports are only show a real CNPJ validation
  from django_stuff.utils import remove_special_characters
  from django_stuff.validators import validate_cnpj

  ...

  class CompanyExampleForm(DynamicForm):

      class Meta:
          dynamic_fields = {
              'name': _("Company Name"),
              'brand': _("Brand"),
              'cnpj': _("CNPJ"),
          }

      def clean_cnpj(self):
          value = remove_special_characters(self.cleaned_data['cnpj'])
          if not validate_cnpj(value):
              raise forms.ValidationError("CNPJ Invalid.")
          return value



AjaxChoiceField
---------------

Is the same of a ChoiceField but you are able to populate the choices using ``ajax`` directly from the template and submit the result

- Example

.. code-block:: python

    from django_api_client.fields import AjaxChoiceField

    ...
    class TestForm(DynamicForm):
        sub_category = AjaxChoiceField(label=_("Sub Category"), widget=forms.Select)

        class Meta:
          dynamic_fields = {
              ...
              'sub_category':,
          }
