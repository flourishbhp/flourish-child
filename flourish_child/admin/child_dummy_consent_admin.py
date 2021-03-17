from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_child_admin
from ..forms import ChildDummySubjectConsentForm
from ..models import ChildDummySubjectConsent
from .model_admin_mixins import ModelAdminMixin


@admin.register(ChildDummySubjectConsent, site=flourish_child_admin)
class ChildDummySubjectConsentAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = ChildDummySubjectConsentForm

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
                'consent_datetime',
                'identity',
                'dob',
                'gender',
                'guardian_name',
                'subject_type',
                'cohort']}
         ), audit_fieldset_tuple)

    radio_fields = {
                    'gender': admin.VERTICAL,
                    'cohort': admin.VERTICAL}

