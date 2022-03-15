from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import InfantDevScreening36MonthsForm
from ..models import InfantDevScreening36Months


@admin.register(InfantDevScreening36Months, site=flourish_child_admin)
class InfantDevScreening36MonthsAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    form = InfantDevScreening36MonthsForm

    fieldsets = (
        (None, {
            'fields': (
                'child_visit',
                'report_datetime',
                'speaking',
                'hearing_specialist',
                'vision',
                'vision_specialist',
                'play_with_people',
                'play_with_toys',
                'cognitive_specialist',
                'runs_well',
                'self_feed',
                'motor_skills_specialist',
                'caregiver_concerns',
            )
        }), audit_fieldset_tuple
    )

    additional_instructions = ('Respond ‘Yes’ to any question where the caregiver says'
                               ' that the child CAN do the following')

    radio_fields = {"speaking": admin.VERTICAL,
                    "hearing_specialist": admin.VERTICAL,
                    "vision": admin.VERTICAL,
                    "vision_specialist": admin.VERTICAL,
                    "play_with_people": admin.VERTICAL,
                    "play_with_toys": admin.VERTICAL,
                    "cognitive_specialist": admin.VERTICAL,
                    "runs_well": admin.VERTICAL,
                    "self_feed": admin.VERTICAL,
                    "motor_skills_specialist": admin.VERTICAL,
                    }
