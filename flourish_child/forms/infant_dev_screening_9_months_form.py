from django import forms

from flourish_child.forms.child_form_mixin import ChildModelFormMixin
from ..models.infant_dev_screening_9_months import InfantDevScreening9Months


class InfantDevScreening9MonthsForm(ChildModelFormMixin, forms.ModelForm):
    class Meta:
        model = InfantDevScreening9Months
        fields = '__all__'
