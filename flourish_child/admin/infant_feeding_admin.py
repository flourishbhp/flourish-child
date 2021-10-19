from django.contrib import admin
from edc_fieldsets.fieldlist import Insert
from edc_fieldsets.fieldsets_modeladmin_mixin import FormLabel
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_child_admin
from ..forms import InfantFeedingForm
from ..models import InfantFeeding
from .model_admin_mixins import ChildCrfModelAdminMixin


@admin.register(InfantFeeding, site=flourish_child_admin)
class InfantFeedingAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = InfantFeedingForm
    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'ever_breastfed',
                'bf_start_dt',
                'bf_start_dt_est',
                'recent_bf_dt',
                'continuing_to_bf',
                'dt_weaned',
                'freq_milk_rec',
                'rec_liquids',
                'taken_formula',
                'dt_formula_introduced',
                'dt_formula_est',
                'formula_feedng_completd',
                'dt_formula_stopd',
                'dt_stopd_est',
                'formula_water',
                'formula_water_other',
                'taken_water',
                'taken_juice',
                'taken_cows_milk',
                'cows_milk_used',
                'taken_animal_milk',
                'animal_milk_specify',
                'milk_boiled',
                'taken_salts',
                'taken_solid_foods', ]
        }),
        ('Solid Food Section', {
            'fields': [
                'solid_foods_dt',
                'solid_foods_age',
                'solid_foods',
                'grain_intake_freq',
                'legumes_intake_freq',
                'dairy_intake_freq',
                'flesh_foods_freq',
                'eggs_intake_freq',
                'porridge_intake_freq',
                'vitamin_a_fruits_freq',
                'other_fruits_vegies',
                'other_fruits_freq',
                'other_solids',
                'other_solids_freq', ]
        }),
        audit_fieldset_tuple
    )

    radio_fields = {
        'ever_breastfed': admin.VERTICAL,
        'bf_start_dt_est': admin.VERTICAL,
        'continuing_to_bf': admin.VERTICAL,
        'freq_milk_rec': admin.VERTICAL,
        'rec_liquids': admin.VERTICAL,
        'taken_formula': admin.VERTICAL,
        'dt_formula_est': admin.VERTICAL,
        'formula_feedng_completd': admin.VERTICAL,
        'dt_stopd_est': admin.VERTICAL,
        'formula_water': admin.VERTICAL,
        'taken_water': admin.VERTICAL,
        'taken_juice': admin.VERTICAL,
        'taken_cows_milk': admin.VERTICAL,
        'cows_milk_used': admin.VERTICAL,
        'taken_animal_milk': admin.VERTICAL,
        'milk_boiled': admin.VERTICAL,
        'taken_salts': admin.VERTICAL,
        'taken_solid_foods': admin.VERTICAL,
        'infant_feeding_changed': admin.VERTICAL, }

    filter_horizontal = ('solid_foods', )

    list_display = ('child_visit', 'report_datetime', 'last_att_sche_visit', )

    custom_form_labels = [
        FormLabel(
            field='infant_feeding_changed',
            label=('Since the last scheduled visit in {previous}, has any of '
                   'your infant feeding information changed?'),
            previous_appointment=True)
    ]

    schedules = ['child_a_sec_schedule1', 'child_a_quart_schedule1',
                 'child_b_sec_schedule1', 'child_b_quart_schedule1',
                 'child_c_sec_schedule1', 'child_c_quart_schedule1',
                 'child_pool_schedule1']

    conditional_fieldlists = {}
    for schedule in schedules:
        conditional_fieldlists.update({schedule: Insert(
            'last_att_sche_visit', 'infant_feeding_changed',
            after='report_datetime')})

    def get_form(self, request, obj=None, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        form.previous_instance = self.get_previous_instance(request)
        return form
