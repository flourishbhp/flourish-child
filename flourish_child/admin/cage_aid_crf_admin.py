from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from flourish_child.models import ChildCageAid
from flourish_child.forms import ChildCageAidForm


@admin.register(ChildCageAid, site=flourish_child_admin)
class ChildCageAidAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = ChildCageAidForm

    fieldsets = (
        (None, {
            'fields': (
                'child_visit',
                'report_datetime',
                'alcohol_drugs',
                'cut_down',
                'people_reaction',
                'guilt',
                'eye_opener',

            )}
         ), audit_fieldset_tuple)

    radio_fields = {
        'alcohol_drugs': admin.VERTICAL,
        'cut_down': admin.VERTICAL,
        'people_reaction': admin.VERTICAL,
        'guilt': admin.VERTICAL,
        'eye_opener': admin.VERTICAL,
    }
