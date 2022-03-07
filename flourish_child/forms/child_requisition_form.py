from arrow.arrow import Arrow
from django import forms
from django.conf import settings
from django.utils import timezone
from edc_base.utils import convert_php_dateformat
from edc_form_validators import FormValidatorMixin
from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
from edc_visit_tracking.crf_date_validator import CrfDateValidator
from edc_visit_tracking.crf_date_validator import (
    CrfReportDateAllowanceError, CrfReportDateBeforeStudyStart)
from edc_visit_tracking.crf_date_validator import CrfReportDateIsFuture
from edc_lab.forms.modelform_mixins import RequisitionFormMixin

from flourish_child.models.child_visit import ChildVisit
from .child_form_mixin import ChildModelFormMixin
from ..models import ChildRequisition


class InlineSubjectModelFormMixin(FormValidatorMixin, forms.ModelForm):

    visit_model = ChildVisit


class ChildRequisitionForm(ChildModelFormMixin, RequisitionFormMixin,
                           FormValidatorMixin):

    requisition_identifier = forms.CharField(
        label='Requisition identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'child_visit').subject_identifier
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
                    f'Invalid. Cannot be before date of visit {formatted}.'})

    def validate_other_specify_field(self, form_validator=None):
        form_validator.validate_other_specify(
            field='reason_not_drawn', other_stored_value='other')

    class Meta:
        model = ChildRequisition
        fields = '__all__'
