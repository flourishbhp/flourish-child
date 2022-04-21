from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms.infant_dev_screening_9_months_form import InfantDevScreening9MonthsForm
from ..models.infant_dev_screening_9_months import InfantDevScreening9Months


@admin.register(InfantDevScreening9Months, site=flourish_child_admin)
class InfantDevScreening9MonthsAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    form = InfantDevScreening9MonthsForm

    fieldsets = (
        (None, {
            'fields': (
                'child_visit',
                'report_datetime',
                'speaking',
                'hearing',
                'speaking_specialist',
                'vision',
                'vision_specialist',
                'cognitive_behavior',
                'cognitive_behavior_reactions',
                'cognitive_specialist',
                'sits',
                'moves_objects',
                'motor_skills_specialist',
                'caregiver_concerns',
                )
            }), audit_fieldset_tuple
        )

    additional_instructions = ('Respond ‘Yes’ to any question where the caregiver says'
                               ' that the child CAN do the following')

    radio_fields = {"speaking": admin.VERTICAL,
                    "hearing": admin.VERTICAL,
                    "speaking_specialist": admin.VERTICAL,
                    "vision": admin.VERTICAL,
                    "vision_specialist": admin.VERTICAL,
                    "cognitive_behavior": admin.VERTICAL,
                    "cognitive_behavior_reactions": admin.VERTICAL,
                    "cognitive_specialist": admin.VERTICAL,
                    "sits": admin.VERTICAL,
                    "moves_objects": admin.VERTICAL,
                    "motor_skills_specialist": admin.VERTICAL,
                    }
