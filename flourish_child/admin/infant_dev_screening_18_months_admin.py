from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import InfantDevScreening18MonthsForm
from ..models import InfantDevScreening18Months


@admin.register(InfantDevScreening18Months, site=flourish_child_admin)
class InfantDevScreening18MonthsAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    form = InfantDevScreening18MonthsForm

    fieldsets = (
        (None, {
            'fields': [
                'speaking',
                'speaking_specialist',
                'vision',
                'vision_specialist',
                'cognitive_behavior',
                'cognitive_specialist',
                'walks',
                'self_feed',
                'motor_skills_specialist',
                'caregiver_concerns',
            ]
        }), audit_fieldset_tuple
    )

    radio_fields = {"speaking": admin.VERTICAL,
                    "speaking_specialist": admin.VERTICAL,
                    "vision": admin.VERTICAL,
                    "vision_specialist": admin.VERTICAL,
                    "cognitive_behavior": admin.VERTICAL,
                    "cognitive_specialist": admin.VERTICAL,
                    "walks": admin.VERTICAL,
                    "self_feed": admin.VERTICAL,
                    "motor_skills_specialist": admin.VERTICAL,
                    }
