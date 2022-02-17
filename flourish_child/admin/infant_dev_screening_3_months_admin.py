from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms.infant_dev_screening_3_months_form import InfantDevScreening3MonthsForm
from ..models.infant_dev_screening_3_months import InfantDevScreening3Months


@admin.register(InfantDevScreening3Months, site=flourish_child_admin)
class InfantDevScreening3MonthsAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    form = InfantDevScreening3MonthsForm

    fieldsets = (
        (None, {
            'fields': [
                'hearing',
                'hearing_specialist',
                'vision',
                'vision_specialist',
                'cognitive_behavior',
                'cognitive_specialist',
                'motor_skills_head',
                'motor_skills_hands',
                'motor_skills_specialist',
                'caregiver_concerns',
            ]
        }), audit_fieldset_tuple
    )

    radio_fields = {"hearing": admin.VERTICAL,
                    "hearing_specialist": admin.VERTICAL,
                    "vision": admin.VERTICAL,
                    "vision_specialist": admin.VERTICAL,
                    "cognitive_behavior": admin.VERTICAL,
                    "cognitive_specialist": admin.VERTICAL,
                    "motor_skills_head": admin.VERTICAL,
                    "motor_skills_hands": admin.VERTICAL,
                    "motor_skills_specialist": admin.VERTICAL,
                    }
