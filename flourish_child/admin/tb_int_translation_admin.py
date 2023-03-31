from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import TbInterviewTranslationForm
from ..models import TbAdolInterviewTranslation


@admin.register(TbAdolInterviewTranslation, site=flourish_child_admin)
class TbInterviewTranslationAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    form = TbInterviewTranslationForm

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'translation_date',
                'translator_name',
                'interview_translation',
            ]}
         ), audit_fieldset_tuple)
