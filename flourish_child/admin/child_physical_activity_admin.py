from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import ChildPhysicalActivityForm
from ..models import ChildPhysicalActivity


@admin.register(ChildPhysicalActivity, site=flourish_child_admin)
class ChildPhysicalActivityAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = ChildPhysicalActivityForm

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'vig_activity_days',
                'specify_vig_days',
                'vig_activity_time',
                'specify_vig_time_hrs',
                'specify_vig_time_mins',
                'mod_activity_days',
                'specify_mod_days',
                'mod_activity_time',
                'specify_mod_time_hrs',
                'specify_mod_time_mins',
                'walking_days',
                'specify_walk_days',
                'walking_time',
                'specify_walk_time_hrs',
                'specify_walk_time_mins',
                'sitting_time',
                'specify_sit_time_hrs',
                'specify_sit_time_mins'
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'vig_activity_days': admin.VERTICAL,
                    'vig_activity_time': admin.VERTICAL,
                    'mod_activity_days': admin.VERTICAL,
                    'mod_activity_time': admin.VERTICAL,
                    'walking_days': admin.VERTICAL,
                    'walking_time': admin.VERTICAL,
                    'sitting_time': admin.VERTICAL, }
