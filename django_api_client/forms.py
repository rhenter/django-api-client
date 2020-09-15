from django import forms
from django.forms import BaseForm
from django.forms.fields import Field
from django.forms.widgets import MediaDefiningClass
from django.utils.translation import gettext_lazy as _

from .utils import labelize


class DeclarativeFieldsMetaclass(MediaDefiningClass):
    """Collect Fields declared on the base classes."""

    def __new__(mcs, name, bases, attrs):
        # Collect fields from current class.
        current_fields = []
        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                current_fields.append((key, value))
                attrs.pop(key)

        meta = attrs.get('Meta', None)
        dynamic_fields = getattr(meta, 'dynamic_fields', '')
        if meta and dynamic_fields:
            if isinstance(dynamic_fields, dict):
                for field_name, field_label in dynamic_fields.items():
                    if any([field_name in key for key in current_fields]):
                        continue
                    current_fields.append((field_name, forms.CharField(label=_(field_label))))
            elif isinstance(dynamic_fields, list) or isinstance(dynamic_fields, tuple):
                for field_name in dynamic_fields:
                    if any([field_name in key for key in current_fields]):
                        continue
                    current_fields.append((field_name, forms.CharField(label=labelize(field_name))))
            else:
                dynamic_fields = dict(current_fields).keys()

            for field_name, field in current_fields:
                assert field_name in dynamic_fields, (
                    "The field '{field_name}' was declared on DynamicForm "
                    "{form_class}, but has not been included in the "
                    "'dynamic_fields' option.".format(
                        field_name=field_name,
                        form_class=name
                    )
                )

            current_fields = sorted(current_fields, key=lambda pair: list(dynamic_fields).index(pair[0]))

        attrs['declared_fields'] = dict(current_fields)
        new_class = super(DeclarativeFieldsMetaclass, mcs).__new__(mcs, name, bases, attrs)

        # Walk through the MRO.
        declared_fields = {}
        for base in reversed(new_class.__mro__):
            # Collect fields from base class.
            if hasattr(base, 'declared_fields'):
                declared_fields.update(base.declared_fields)

            # Field shadowing.
            for attr, value in base.__dict__.items():
                if value is None and attr in declared_fields:
                    declared_fields.pop(attr)

        new_class.base_fields = declared_fields
        new_class.declared_fields = declared_fields

        return new_class


class DynamicForm(BaseForm, metaclass=DeclarativeFieldsMetaclass):
    "A collection of Fields, plus their associated data."
    # This is a separate class from BaseForm in order to abstract the way
    # self.fields is specified. This class (Form) is the one that does the
    # fancy metaclass stuff purely for the semantic sugar -- it allows one
    # to define a form using declarative syntax.
    # BaseForm itself has no way of designating self.fields.
