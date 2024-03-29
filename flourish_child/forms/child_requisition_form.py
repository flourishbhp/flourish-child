from flourish_child.models.child_visit import ChildVisit

from arrow.arrow import Arrow
from django import forms
from django.conf import settings
from django.utils import timezone
from edc_base.utils import convert_php_dateformat
from edc_form_validators import FormValidatorMixin
from edc_lab.forms.modelform_mixins import RequisitionFormMixin
from edc_senaite_interface.forms import SenaiteRequisitionFormValidatorMixin

from ..models import ChildRequisition
from .child_form_mixin import ChildModelFormMixin


class InlineSubjectModelFormMixin(FormValidatorMixin, forms.ModelForm):
    visit_model = ChildVisit


class ChildRequisitionForm(ChildModelFormMixin, RequisitionFormMixin,
                           SenaiteRequisitionFormValidatorMixin,
                           FormValidatorMixin):

    requisition_identifier = forms.CharField(
        label='Requisition identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def clean(self):
        self.visit_obj = self.cleaned_data.get('child_visit')
        self.subject_identifier = self.cleaned_data.get(
            'child_visit').subject_identifier
        self.validate_requisition_datetime()
        super().clean()

    def validate_requisition_datetime(self):
        requisition_datetime = self.cleaned_data.get('requisition_datetime')
        child_visit = self.cleaned_data.get('child_visit')
        if requisition_datetime:
            requisition_datetime = Arrow.fromdatetime(
                requisition_datetime, requisition_datetime.tzinfo).to('utc').datetime
            if requisition_datetime < child_visit.report_datetime:
                formatted = timezone.localtime(child_visit.report_datetime).strftime(
                    convert_php_dateformat(settings.SHORT_DATETIME_FORMAT))
                raise forms.ValidationError({
                    'requisition_datetime':
                        f'Invalid. Cannot be before date of visit {formatted}.'
                    })

    class Meta:
        model = ChildRequisition
        fields = '__all__'
