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
                'lost_friends_period',
                'bullied',
                'bullied_period',
            ]},
        ),
        ('Because someone else in my family has HIV, I have experienced discrimination at:', {
            'fields': [
                'home_discr',
                'home_discr_period',
                'neighborhood_discr',
                'neighborhood_discr_period',
                'religious_place_discr',
                'religious_place_discr_period',
                'clinic_discr',
                'clinic_discr_period',
                'school_discr',
                'school_discr_period',
                'other_place_discr',
                'other_place_discr_period',
            ]},
         ),
        ('Because someone else in my family has HIV, discrimination has led to my family to:', {
            'fields': [
                'lose_fin_support',
                'lose_fin_support_period',
                'lose_social_support',
                'lose_social_support_period',

            ]}
         ),

        ('Because someone else in my family has HIV, discrimination has made me feel:', {
            'fields': [
                'stressed_or_anxious',
                'stressed_or_anxious_period',
                'depressed_or_sad',
                'depressed_or_sad_period'

            ]}
         ), audit_fieldset_tuple)

    radio_fields = {
        'lost_friends': admin.VERTICAL,
        'lost_friends_period': admin.VERTICAL,
        'bullied': admin.VERTICAL,
        'bullied_period': admin.VERTICAL,
        'home_discr': admin.VERTICAL,
        'home_discr_period': admin.VERTICAL,
        'neighborhood_discr': admin.VERTICAL,
        'neighborhood_discr_period': admin.VERTICAL,
        'religious_place_discr': admin.VERTICAL,
        'religious_place_discr_period': admin.VERTICAL,
        'clinic_discr': admin.VERTICAL,
        'clinic_discr_period': admin.VERTICAL,
        'school_discr': admin.VERTICAL,
        'school_discr_period': admin.VERTICAL,
        'other_place_discr_period': admin.VERTICAL,
        'lose_fin_support': admin.VERTICAL,
        'lose_fin_support_period': admin.VERTICAL,
        'lose_social_support': admin.VERTICAL,
        'lose_social_support_period': admin.VERTICAL,
        'stressed_or_anxious': admin.VERTICAL,
        'stressed_or_anxious_period': admin.VERTICAL,
        'depressed_or_sad': admin.VERTICAL,
        'depressed_or_sad_period': admin.VERTICAL
    }
