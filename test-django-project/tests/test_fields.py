import pytest
from django.core.exceptions import ValidationError

from django_api_client.fields import AjaxChoiceField


@pytest.mark.parametrize('value', [
    '',
    None,
])
def test_choicefield_required(value):
    f = AjaxChoiceField(choices=[('1', 'One'), ('2', 'Two')], required=True)
    with pytest.raises(ValidationError) as error:
        f.clean(value)
    assert str(error) != "'This field is required.'"


@pytest.mark.parametrize('value', [4, 5, 6])
def test_choicefield_invalid(value):
    """This field should be filled by ajax, so the should not validate the choice"""
    f = AjaxChoiceField(choices=[('1', 'One'), ('2', 'Two')], required=False)

    assert str(value) == f.clean(value)


def test_choicefield_valid():
    f = AjaxChoiceField(choices=[('1', 'One'), ('2', 'Two')], required=False)

    assert '1' == f.clean(1)
    assert '2' == f.clean(2)


def test_choicefield_callable():
    def choices():
        return [('J', 'John'), ('P', 'Paul')]

    f = AjaxChoiceField(choices=choices)
    assert 'J' == f.clean('J')
