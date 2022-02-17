from django import forms

from flourish_child.forms.child_form_mixin import ChildModelFormMixin
from ..models.infant_dev_screening_3_months import InfantDevScreening3Months


class InfantDevScreening3MonthsForm(ChildModelFormMixin, forms.ModelForm):
    class Meta:
        model = InfantDevScreening3Months
        fields = '__all__'
