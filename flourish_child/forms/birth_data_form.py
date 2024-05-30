from django import forms

from flourish_child_validations.form_validators import BirthDataFormValidator
from .child_form_mixin import ChildModelFormMixin
from ..models import BirthData
from ..helper_classes.utils import child_utils


class BirthDataForm(ChildModelFormMixin):
    form_validator_cls = BirthDataFormValidator

    gestational_age = forms.DecimalField(
        label="What is the infant's determined gestational age: ",
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    def __init__(self, *args, **kwargs):
        super(BirthDataForm, self).__init__(*args, **kwargs)
        child_visit = self.child_visit_obj
        subject_identifier = getattr(child_visit, 'subject_identifier', '')
        gestational_age = self.initial.get('gestational_age', None)
        if not gestational_age:
            self.initial['gestational_age'] = child_utils.get_gestational_age(
                subject_identifier)

    @property
    def child_visit_obj(self):
        try:
            return self.visit_model.objects.get(
                id=self.initial.get('child_visit'))
        except self.visit_model.DoesNotExist:
            return None

    class Meta:
        model = BirthData
        fields = '__all__'
