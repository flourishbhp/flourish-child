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
                'first_name',
                'last_name',
                'initials',
                'dob',
                'is_dob_estimated',
                'gender',
                'guardian_name',
                'subject_type',
                'cohort']}
         ), audit_fieldset_tuple)

    list_display = (
        'consent_datetime',
        'first_name',
        'last_name',
        'initials',
        'dob',
        'gender',
    )

    radio_fields = {'is_dob_estimated': admin.VERTICAL,
                    'gender': admin.VERTICAL,
                    'cohort': admin.VERTICAL}

