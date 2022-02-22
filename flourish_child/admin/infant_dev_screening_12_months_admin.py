from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import InfantDevScreening12MonthsForm
from ..models import InfantDevScreening12Months


@admin.register(InfantDevScreening12Months, site=flourish_child_admin)
class InfantDevScreening12MonthsAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    form = InfantDevScreening12MonthsForm

    fieldsets = (
        (None, {
            'fields': [
                'hearing',
                'hearing_response',
                'hearing_communication',
                'hearing_specialist',
                'eye_movement',
                'familiar_obj',
                'vision_specialist',
                'cognitive_behavior',
                'understands',
                'cognitive_specialist',
                'stands',
                'picks_objects',
                'motor_skills_specialist',
                'caregiver_concerns',
            ]
        }), audit_fieldset_tuple
    )

    radio_fields = {"hearing": admin.VERTICAL,
                    "hearing_response": admin.VERTICAL,
                    "hearing_communication": admin.VERTICAL,
                    "hearing_specialist": admin.VERTICAL,
                    "eye_movement": admin.VERTICAL,
                    "familiar_obj": admin.VERTICAL,
                    "vision_specialist": admin.VERTICAL,
                    "cognitive_behavior": admin.VERTICAL,
                    "cognitive_specialist": admin.VERTICAL,
                    "understands": admin.VERTICAL,
                    "stands": admin.VERTICAL,
                    "picks_objects": admin.VERTICAL,
                    "motor_skills_specialist": admin.VERTICAL,
                    }
