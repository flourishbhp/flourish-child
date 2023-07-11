from django import forms
from django.apps import apps as django_apps
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
from edc_visit_tracking.crf_date_validator import CrfDateValidator
from edc_visit_tracking.crf_date_validator import (
    CrfReportDateAllowanceError, CrfReportDateBeforeStudyStart)
from edc_visit_tracking.crf_date_validator import CrfReportDateIsFuture
from edc_visit_tracking.modelform_mixins import VisitTrackingModelFormMixin

from ..models import ChildVisit


class ChildModelFormMixin(
    SiteModelFormMixin, VisitTrackingModelFormMixin,
    FormValidatorMixin, forms.ModelForm):
    visit_model = ChildVisit

    def clean(self):
        cleaned_data = super().clean()
        if (cleaned_data.get('child_visit')
                and cleaned_data.get('child_visit').visit_code):
            if cleaned_data.get('report_datetime'):
                try:
                    CrfDateValidator(
                        report_datetime=cleaned_data.get('report_datetime'),
                        visit_report_datetime=cleaned_data.get(
                            self._meta.model.visit_model_attr()).report_datetime)
                except (CrfReportDateAllowanceError, CrfReportDateBeforeStudyStart,
                        CrfReportDateIsFuture) as e:
                    raise forms.ValidationError(e)
        return cleaned_data

    @property
    def registered_subject_model_cls(self):
        return django_apps.get_model('edc_registration.registeredsubject')

    @property
    def caregiver_subject_identifier(self):
        subject_identifier = self.initial.get('subject_identifier', None)
        try:
            return self.registered_subject_model_cls.objects.get(
                subject_identifier=subject_identifier).relative_identifier
        except self.registered_subject_model_cls.DoesNotExist:
            return None


class InlineChildModelFormMixin(FormValidatorMixin, forms.ModelForm):
    visit_model = ChildVisit
