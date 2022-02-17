from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import InfantDevScreening60To72MonthsForm
from ..models import InfantDevScreening60To72Months


@admin.register(InfantDevScreening60To72Months, site=flourish_child_admin)
class InfantDevScreening60To72MonthsAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    form = InfantDevScreening60To72MonthsForm

    fieldsets = (
        (None, {
            'fields': [
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
            ]
        }), audit_fieldset_tuple
    )

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
