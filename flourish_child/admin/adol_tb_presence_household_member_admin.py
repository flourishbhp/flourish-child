from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_child_admin
from ..forms import TbPresenceHouseholdMembersAdolForm
from ..models import TbPresenceHouseholdMembersAdol
from .model_admin_mixins import ChildCrfModelAdminMixin


@admin.register(TbPresenceHouseholdMembersAdol, site=flourish_child_admin)
class TbPresenceHouseholdMembersAdolAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = TbPresenceHouseholdMembersAdolForm

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'tb_diagnosed',
                'tb_ind_rel',
                'tb_ind_other',
                'tb_referral',
                'tb_in_house',
                'cough_ind_rel',
                'cough_ind_other',
                'fever_signs',
                'fever_ind_rel',
                'fever_ind_other',
                'night_sweats',
                'sweat_ind_rel',
                'sweat_ind_other',
                'weight_loss',
                'weight_ind_rel',
                'weight_ind_other',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'tb_diagnosed': admin.VERTICAL,
                    'tb_ind_rel': admin.VERTICAL,
                    'tb_referral': admin.VERTICAL,
                    'tb_in_house': admin.VERTICAL,
                    'cough_ind_rel': admin.VERTICAL,
                    'fever_signs': admin.VERTICAL,
                    'fever_ind_rel': admin.VERTICAL,
                    'night_sweats': admin.VERTICAL,
                    'sweat_ind_rel': admin.VERTICAL,
                    'weight_loss': admin.VERTICAL,
                    'weight_ind_rel': admin.VERTICAL}
