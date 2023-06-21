from django import forms

from .child_form_mixin import ChildModelFormMixin

from ..models import TbReferalAdol


class TbReferralAdolForm(ChildModelFormMixin):

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = TbReferalAdol
        fields = '__all__'
