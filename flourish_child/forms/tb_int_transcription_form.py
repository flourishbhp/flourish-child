from django import forms

from .child_form_mixin import ChildModelFormMixin
from ..models import TbAdolInterviewTranscription


class TbInterviewTranscriptionForm(ChildModelFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['transcriber_name'].widget = forms.RadioSelect(
            choices=self.instance.intv_users)

    class Meta:
        model = TbAdolInterviewTranscription
        fields = '__all__'
