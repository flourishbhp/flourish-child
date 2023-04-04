from django import forms

from flourish_child.forms.child_form_mixin import ChildModelFormMixin
from ..models import InfantDevScreening36Months


class InfantDevScreening36MonthsForm(ChildModelFormMixin, forms.ModelForm):
    class Meta:
        model = InfantDevScreening36Months
        fields = '__all__'
