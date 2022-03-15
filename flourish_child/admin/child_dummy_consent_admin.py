from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import ChildDummySubjectConsentForm
from ..models import ChildDummySubjectConsent


@admin.register(ChildDummySubjectConsent, site=flourish_child_admin)
class ChildDummySubjectConsentAdmin(ModelAdminMixin, admin.ModelAdmin):
    form = ChildDummySubjectConsentForm

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
                'consent_datetime',
                'dob',
                'cohort']
            }
         ), audit_fieldset_tuple)

    list_display = ('dob', 'cohort')

    list_filter = (
        'dob',
        'cohort'
        )

    preserve_filters = (
        'dob',
        'cohort'
    )

    radio_fields = {'cohort': admin.VERTICAL}
