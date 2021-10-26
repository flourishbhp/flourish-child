from django import forms
from django.apps import apps as django_apps
from edc_action_item.site_action_items import site_action_items
from edc_base.sites import SiteModelFormMixin
from edc_constants.constants import NEW
from edc_form_validators import FormValidatorMixin
from flourish_child_validations.form_validators import ChildVisitFormValidator

from ..action_items import CHILDCONTINUEDCONSENT_STUDY_ACTION, CHILDASSENT_ACTION
from ..models import ChildVisit


class ChildVisitForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = ChildVisitFormValidator

    def clean(self):
        super().clean()
        subject_identifier = self.cleaned_data.get('appointment').subject_identifier

        # Validate incomplete continued consent form if child >= 18 years of age..
        self.validate_incomplete_required_model(
            subject_identifier=subject_identifier,
            model='flourish_child.childcontinuedconsent',
            action_name=CHILDCONTINUEDCONSENT_STUDY_ACTION,
            msg=('Participant is 18 years of age, cannot edit visit until '
                 'participant has given their continued consent for participation.'))

        # Validate incomplete child assent form if child >= 7 years of age.
        self.validate_incomplete_required_model(
            subject_identifier=subject_identifier,
            model='flourish_child.childassent',
            action_name=CHILDASSENT_ACTION,
            msg=('Participant is older than 7 years, please complete the child'
                 ' assent form before continuing with the visits.'))

    def validate_incomplete_required_model(
            self, subject_identifier=None, model=None, action_name=None, msg=None):
        model_cls = django_apps.get_model(model)
        action_cls = site_action_items.get(model_cls.action_name)
        action_item_model_cls = action_cls.action_item_model_cls()
        try:
            action_item_model_cls.objects.get(
                subject_identifier=subject_identifier,
                action_type__name=action_name,
                status=NEW)
        except action_item_model_cls.DoesNotExist:
            try:
                model_obj = model_cls.objects.get(
                    subject_identifier=subject_identifier,
                    version='1')
            except model_cls.DoesNotExist:
                pass
            else:
                if not model_obj.is_eligible:
                    raise forms.ValidationError(
                        'Participant is not eligible for study participation '
                        f'on the {model_cls._meta.verbose_name}. Can not edit '
                        'visit, should be taken off study.')
        else:
            raise forms.ValidationError(msg)

    class Meta:
        model = ChildVisit
        fields = '__all__'
