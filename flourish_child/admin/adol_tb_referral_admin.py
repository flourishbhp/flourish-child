from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from ..forms import TbReferralAdolForm
from ..models import TbReferalAdol
from ..admin_site import flourish_child_admin

from .model_admin_mixins import ChildCrfModelAdminMixin


@admin.register(TbReferalAdol, site=flourish_child_admin)
class TbReferralAdolAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = TbReferralAdolForm

    search_fields = ('subject_identifier',)

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'referral_date',
                'location',
                'location_other']}
         ), audit_fieldset_tuple)


