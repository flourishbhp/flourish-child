from django import forms

from flourish_child.forms.child_form_mixin import ChildModelFormMixin
from ..models import InfantDevScreening60To72Months


class InfantDevScreening60To72MonthsForm(ChildModelFormMixin, forms.ModelForm):
    class Meta:
        model = InfantDevScreening60To72Months
        fields = '__all__'
