from django import forms

from flourish_child.forms.child_form_mixin import ChildModelFormMixin
from ..models import InfantDevScreening18Months


class InfantDevScreening18MonthsForm(ChildModelFormMixin, forms.ModelForm):
    class Meta:
        model = InfantDevScreening18Months
        fields = '__all__'
