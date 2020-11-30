from django import forms

from .child_form_mixin import ChildModelFormMixin
from ..models import ChildGadAnxietyScreening


class ChildGadAnxietyScreeningForm(ChildModelFormMixin, forms.ModelForm):

    class Meta:
        model = ChildGadAnxietyScreening
        fields = '__all__'
