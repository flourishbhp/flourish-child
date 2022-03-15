from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import InfantDevScreening72MonthsForm
from ..models import InfantDevScreening72Months


@admin.register(InfantDevScreening72Months, site=flourish_child_admin)
class InfantDevScreening72MonthsAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    form = InfantDevScreening72MonthsForm

    fieldsets = (
        (None, {
            'fields': (
                'child_visit',
                'report_datetime',
                'speak',
                'hearing_response',
                'hearing_specialist',
                'vision_problems',
                'vision_specialist',
                'interactive',
                'understand_commands',
                'cognitive_specialist',
                'motor_skills_hops',
                'motor_skills_drawing',
                'motor_skills_dress',
                'motor_skills_specialist',
                'caregiver_concerns',
            )
        }), audit_fieldset_tuple
    )

    additional_instructions = ('Respond ‘Yes’ to any question where the caregiver says'
                               ' that the child CAN do the following')

    radio_fields = {"speak": admin.VERTICAL,
                    "hearing_response": admin.VERTICAL,
                    "hearing_specialist": admin.VERTICAL,
                    "vision_problems": admin.VERTICAL,
                    "vision_specialist": admin.VERTICAL,
                    "interactive": admin.VERTICAL,
                    "understand_commands": admin.VERTICAL,
                    "cognitive_specialist": admin.VERTICAL,
                    "motor_skills_hops": admin.VERTICAL,
                    "motor_skills_drawing": admin.VERTICAL,
                    "motor_skills_dress": admin.VERTICAL,
                    "motor_skills_specialist": admin.VERTICAL,
                    }
