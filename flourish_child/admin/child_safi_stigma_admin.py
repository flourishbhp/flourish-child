from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import ChildSafiStigmaForm
from ..models import ChildSafiStigma


@admin.register(ChildSafiStigma, site=flourish_child_admin)
class ChildSafiStigmaAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = ChildSafiStigmaForm

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'lost_friends',
                'lost_friends_happened_when',
                'discriminated',
                'discriminated_when',
                'child_home_discrimination',
                'child_home_discrimination_period',
                'child_neighborhood_discrimination',
                'child_neighborhood_discrimination_period',
                'child_religious_place_discrimination',
                'child_religious_place_discrimination_period',
                'child_clinic_discrimination',
                'child_clinic_discrimination_period',
                'child_school_discrimination',
                'child_school_discrimination_period',
                'child_other_discrimination',
                'child_other_discrimination_other',
                'child_other_discrimination_period',
                'lose_finacial_support',
                'lose_finacial_support_period',
                'lose_social_support',
                'lose_social_support_period',
                'stressed_or_anxious',
                'stressed_or_anxious_period',
                'depressed_or_saddened',
                'depressed_or_saddened_period'


            ]}
         ), audit_fieldset_tuple)

    radio_fields = {
        'lost_friends': admin.VERTICAL,
        'lost_friends_happened_when': admin.VERTICAL,
        'discriminated': admin.VERTICAL,
        'discriminated_when': admin.VERTICAL,
        'child_home_discrimination': admin.VERTICAL,
        'child_home_discrimination_period': admin.VERTICAL,
        'child_neighborhood_discrimination': admin.VERTICAL,
        'child_neighborhood_discrimination_period': admin.VERTICAL,
        'child_religious_place_discrimination': admin.VERTICAL,
        'child_religious_place_discrimination_period': admin.VERTICAL,
        'child_clinic_discrimination': admin.VERTICAL,
        'child_clinic_discrimination_period': admin.VERTICAL,
        'child_school_discrimination': admin.VERTICAL,
        'child_school_discrimination_period': admin.VERTICAL,
        'child_other_discrimination': admin.VERTICAL,
        'child_other_discrimination_period': admin.VERTICAL,
        'lose_finacial_support': admin.VERTICAL,
        'lose_finacial_support_period': admin.VERTICAL,
        'lose_social_support': admin.VERTICAL,
        'lose_social_support_period': admin.VERTICAL,
        'stressed_or_anxious': admin.VERTICAL,
        'stressed_or_anxious_period': admin.VERTICAL,
        'depressed_or_saddened': admin.VERTICAL,
        'depressed_or_saddened_period': admin.VERTICAL
    }
