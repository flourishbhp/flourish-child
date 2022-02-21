from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import InfantDevScreening6MonthsForm
from ..models import InfantDevScreening6Months


@admin.register(InfantDevScreening6Months, site=flourish_child_admin)
class InfantDevScreening6MonthsAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    form = InfantDevScreening6MonthsForm

    fieldsets = (
        (None, {
            'fields': [
                'hearing',
                'hearing_response',
                'hearing_specialist',
                'eye_movement',
                'familiar_faces',
                'looks_at_hands',
                'vision_specialist',
                'cognitive_behavior',
                'diff_cries',
                'cognitive_specialist',
                'motor_skills_hands',
                'motor_skills_tummy',
                'motor_skills_specialist',
                'caregiver_concerns',
            ]
        }), audit_fieldset_tuple
    )

    radio_fields = {"hearing": admin.VERTICAL,
                    "hearing_response": admin.VERTICAL,
                    "hearing_specialist": admin.VERTICAL,
                    "eye_movement": admin.VERTICAL,
                    "familiar_faces": admin.VERTICAL,
                    "looks_at_hands": admin.VERTICAL,
                    "vision_specialist": admin.VERTICAL,
                    "cognitive_behavior": admin.VERTICAL,
                    "cognitive_specialist": admin.VERTICAL,
                    "motor_skills_tummy": admin.VERTICAL,
                    "motor_skills_hands": admin.VERTICAL,
                    "motor_skills_specialist": admin.VERTICAL,
                    "diff_cries": admin.VERTICAL,
                    }
