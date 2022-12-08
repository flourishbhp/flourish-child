from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from ..admin_site import flourish_child_admin
from ..forms import TbReferralAdolForm
from ..models import TbReferalAdol
from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin



@admin.register(TbReferalAdol, site=flourish_child_admin)
class TbReferralAdolAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = TbReferralAdolForm

    search_fields = ('subject_identifier',)

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
                'report_datetime',
                'referral_date',
                'location']}
         ), audit_fieldset_tuple)


