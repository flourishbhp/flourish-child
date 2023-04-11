from django import forms

from flourish_child.forms.child_form_mixin import ChildModelFormMixin
from ..models import InfantDevScreening72Months


class InfantDevScreening72MonthsForm(ChildModelFormMixin, forms.ModelForm):

    class Meta:
        model = InfantDevScreening72Months
        fields = '__all__'
