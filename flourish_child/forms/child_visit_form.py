from django import forms
from django.apps import apps as django_apps
from edc_action_item.site_action_items import site_action_items
from edc_base.sites import SiteModelFormMixin
from edc_constants.constants import NEW
from edc_form_validators import FormValidatorMixin
from flourish_child_validations.form_validators import ChildVisitFormValidator

from ..action_items import CHILDCONTINUEDCONSENT_STUDY_ACTION
from ..models import ChildVisit


class ChildVisitForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = ChildVisitFormValidator

    def clean(self):
        super().clean()
        self.validate_incomplete_continued_consent()

    def validate_incomplete_continued_consent(self):
        subject_identifier = self.cleaned_data.get('appointment').subject_identifier
        continued_consent_cls = django_apps.get_model(
            'flourish_child.childcontinuedconsent')
        action_cls = site_action_items.get(
            continued_consent_cls.action_name)
        action_item_model_cls = action_cls.action_item_model_cls()

        try:
            action_item_model_cls.objects.get(
                subject_identifier=subject_identifier,
                action_type__name=CHILDCONTINUEDCONSENT_STUDY_ACTION,
                status=NEW)
        except action_item_model_cls.DoesNotExist:
            try:
                consent_obj = continued_consent_cls.objects.get(
                    subject_identifier=subject_identifier,
                    version='1')
            except continued_consent_cls.DoesNotExist:
                pass
            else:
                if not consent_obj.is_eligible:
                    raise forms.ValidationError(
                        'Participant is not eligible for study participation '
                        'on the continued consent. Can not edit visit, should'
                        ' be taken off study.')
        else:
            raise forms.ValidationError(
                'Participant is 18 years of age, cannot edit visit until'
                ' participant has given their continued consent for participation.')

    class Meta:
        model = ChildVisit
        fields = '__all__'
