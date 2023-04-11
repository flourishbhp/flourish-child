from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_child_admin
from ..forms import ChildTannerStagingForm
from ..models import ChildTannerStaging
from .model_admin_mixins import ChildCrfModelAdminMixin


@admin.register(ChildTannerStaging, site=flourish_child_admin)
class ChildTannerStagingAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = ChildTannerStagingForm

    list_display = ('child_visit', 'assessment_done', 'child_gender', )
    list_filter = ('assessment_done', 'child_gender', )

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'assessment_done',
                'reasons_not_done',
                'child_gender',
                'pubic_hair_stage',
                'breast_stage',
                'manarche_dt_avail',
                'menarche_dt',
                'menarche_dt_est',
                'male_gen_stage',
                'testclr_vol_measrd',
                'rgt_testclr_vol',
                'lft_testclr_vol']}
         ), audit_fieldset_tuple)

    radio_fields = {'assessment_done': admin.VERTICAL,
                    'child_gender': admin.VERTICAL,
                    'breast_stage': admin.VERTICAL,
                    'pubic_hair_stage': admin.VERTICAL,
                    'manarche_dt_avail': admin.VERTICAL,
                    'menarche_dt_est': admin.VERTICAL,
                    'male_gen_stage': admin.VERTICAL,
                    'testclr_vol_measrd': admin.VERTICAL}
