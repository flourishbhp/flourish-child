from django import forms
from flourish_child_validations.form_validators import \
    AcademicPerformanceFormValidator
from ..models import AcademicPerformance
from .child_form_mixin import ChildModelFormMixin


class AcademicPerformanceForm(ChildModelFormMixin):

    form_validator_cls = AcademicPerformanceFormValidator

    education_level = forms.CharField(
        label='What level/class of school is the child currently in?',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = AcademicPerformance
        fields = '__all__'
