from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_base.sites import SiteModelFormMixin
from edc_base.utils import age, get_utcnow
from edc_form_validators import FormValidatorMixin

from flourish_child_validations.form_validators import ChildVisitFormValidator
from ..action_items import CHILDASSENT_ACTION, CHILDCONTINUEDCONSENT_STUDY_ACTION
from ..helper_classes.utils import child_utils
from ..models import ChildVisit


class ChildVisitForm(
    SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):
    form_validator_cls = ChildVisitFormValidator

    def clean(self):
        super().clean()
        self.subject_identifier = self.cleaned_data.get('appointment').subject_identifier
        self.validate_against_onschedule_datetime()

        caregiver_child_consent_obj = child_utils.caregiver_child_consent_obj(
            subject_identifier=self.subject_identifier
        )

        child_age = age(caregiver_child_consent_obj.child_dob, get_utcnow()).years

        if child_age > 17:
            # Validate incomplete continued consent form if child >= 18 years of age..
            self.validate_incomplete_required_model(
                subject_identifier=self.subject_identifier,
                model='flourish_child.childcontinuedconsent',
                action_name=CHILDCONTINUEDCONSENT_STUDY_ACTION,
                msg=('Participant is 18 years of age, cannot edit visit until '
                     'participant has given their continued consent for participation.'))

        if child_age >= 7 and child_age < 18:
            # Validate incomplete child assent form if child >= 7 years of age.
            if not any(
                    item in self.cleaned_data.get('appointment').schedule_name for item in [
                        'quart', 'qt']):
                self.validate_incomplete_required_model(
                    subject_identifier=self.subject_identifier,
                    model='flourish_child.childassent',
                    action_name=CHILDASSENT_ACTION,
                    msg=('Participant is older than 7 years, please complete the child'
                         ' assent form before continuing with the visits.'))

    def validate_incomplete_required_model(
            self, subject_identifier=None, model=None, action_name=None, msg=None):
        model_cls = django_apps.get_model(model)

        consent_version = child_utils.consent_version(
            subject_identifier=subject_identifier)

        try:
            model_obj = model_cls.objects.get(
                subject_identifier=subject_identifier,
                version=consent_version)
        except model_cls.DoesNotExist:
            raise forms.ValidationError(msg)
        else:
            if not model_obj.is_eligible:
                raise forms.ValidationError(
                    'Participant is not eligible for study participation '
                    f'on the {model_cls._meta.verbose_name}. Can not edit '
                    'visit, should be taken off study.')

    def validate_against_onschedule_datetime(self):
        onschedule_model_cls = self.cleaned_data.get(
            'appointment').schedule.onschedule_model_cls
        try:
            onschedule_obj = onschedule_model_cls.objects.get(
                subject_identifier=self.subject_identifier)
        except onschedule_model_cls.DoesNotExist:
            msg = {'__all__': 'OnSchedule object for this visit does not exist.'}
            self._errors.update(msg)
            raise ValidationError(msg)
        else:
            report_datetime = self.cleaned_data.get('report_datetime')
            onschedule_datetime = onschedule_obj.onschedule_datetime
            if report_datetime < onschedule_datetime:
                msg = {'report_datetime':
                           'Report datetime cannot be before Onschedule datetime.'
                           f'Got Report datetime: {report_datetime}, and Onschedule '
                           f'datetime: {onschedule_datetime}'}
                raise ValidationError(msg)

    class Meta:
        model = ChildVisit
        fields = '__all__'
