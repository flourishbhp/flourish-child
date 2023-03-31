from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_child_admin
from ..forms import ChildOffScheduleForm
from ..models import ChildOffSchedule
from .model_admin_mixins import ModelAdminMixin


@admin.register(ChildOffSchedule, site=flourish_child_admin)
class ChildOffScheduleAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = ChildOffScheduleForm

    fieldsets = (
        (None, {
            'fields': [
                'schedule_name',
                'subject_identifier'
            ]}
         ), audit_fieldset_tuple)

    list_filter = ('schedule_name', 'subject_identifier',)
