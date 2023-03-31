from django import forms

from flourish_child.forms.child_form_mixin import ChildModelFormMixin
from ..models import InfantDevScreening12Months


class InfantDevScreening12MonthsForm(ChildModelFormMixin, forms.ModelForm):
    class Meta:
        model = InfantDevScreening12Months
        fields = '__all__'
