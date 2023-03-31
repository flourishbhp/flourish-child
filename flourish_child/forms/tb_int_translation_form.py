from django import forms

from .child_form_mixin import ChildModelFormMixin
from ..models import TbAdolInterviewTranslation


class TbInterviewTranslationForm(ChildModelFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['translator_name'].widget = forms.RadioSelect(
            choices=self.instance.intv_users)

    class Meta:
        model = TbAdolInterviewTranslation
        fields = '__all__'
