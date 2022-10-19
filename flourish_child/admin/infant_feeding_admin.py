from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from edc_fieldsets.fieldlist import Insert
from edc_fieldsets.fieldsets import Fieldsets
from edc_fieldsets.fieldsets_modeladmin_mixin import FormLabel
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_child_admin
from ..forms import InfantFeedingForm
from ..models import InfantFeeding, Appointment
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
                'took_formula',
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
                'cows_milk_prep',
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
        'child_weaned': admin.VERTICAL,
        'freq_milk_rec': admin.VERTICAL,
        'rec_liquids': admin.VERTICAL,
        'took_formula': admin.VERTICAL,
        'formula_first_report': admin.VERTICAL,
        'dt_formula_est': admin.VERTICAL,
        'formula_feedng_completd': admin.VERTICAL,
        'dt_stopd_est': admin.VERTICAL,
        'formula_water': admin.VERTICAL,
        'taken_water': admin.VERTICAL,
        'taken_juice': admin.VERTICAL,
        'taken_cows_milk': admin.VERTICAL,
        'cows_milk_prep': admin.VERTICAL,
        'taken_animal_milk': admin.VERTICAL,
        'milk_boiled': admin.VERTICAL,
        'taken_salts': admin.VERTICAL,
        'taken_solid_foods': admin.VERTICAL,
        'infant_feeding_changed': admin.VERTICAL, }

    filter_horizontal = ('solid_foods',)

    list_display = ('child_visit', 'report_datetime', 'last_att_sche_visit',)

    custom_form_labels = [
        FormLabel(
            field='infant_feeding_changed',
            label=('Since the last scheduled visit in {previous}, has any of '
                   'your infant feeding information changed?'),
            previous_instance=True),
        FormLabel(
            field='continuing_to_bf',
            label=('Since the last visit or quarterly phone call, did the participant '
                   'breast feed?'),
            previous_instance=True),
        FormLabel(
            field='freq_milk_rec',
            label=('Between the last visit or quarterly phone call and date of most recent '
                   'breastfeeding, how often did the participant receive breast milk for '
                   'feeding?'),
            previous_instance=True),
        FormLabel(
            field='rec_liquids',
            label=('Since the last visit or quarterly phone call, has the participant '
                   'received any liquids other than breast milk?'),
            previous_instance=True),
        FormLabel(
            field='took_formula',
            label=('Since the last visit or quarterly phone call, did the participant '
                   'take formula?'),
            previous_instance=True),
        FormLabel(
            field='taken_water',
            label=('Since the last visit or quarterly phone call, did the participant '
                   'take water?'),
            previous_instance=True),
        FormLabel(
            field='taken_juice',
            label=('Since the last visit or quarterly phone call, did the participant '
                   'take juice?'),
            previous_instance=True),
        FormLabel(
            field='taken_cows_milk',
            label=('Since the last visit or quarterly phone call, did the participant '
                   'take cow’s milk?'),
            previous_instance=True),
        FormLabel(
            field='taken_animal_milk',
            label=('Since the last visit or quarterly phone call, did the participant take '
                   'other animal milk?'),
            previous_instance=True),
        FormLabel(
            field='taken_salts',
            label=('Since the last visit or quarterly phone call, did the participant take '
                   'oral rehydration salts?'),
            previous_instance=True),
        FormLabel(
            field='taken_solid_foods',
            label=('Since the last visit or quarterly phone call, has the participant '
                   'received any solid foods?'),
            previous_instance=True)

    ]

    schedules = ['child_a_sec_qt_schedule1', 'child_a_quart_schedule1',
                 'child_b_sec_qt_schedule1', 'child_b_quart_schedule1',
                 'child_c_sec_qt_schedule1', 'child_c_quart_schedule1',
                 'child_pool_schedule1', 'child_a_fu_schedule1', 'child_b_fu_schedule1',
                 'child_c_fu_schedule1']

    enrol_schedules = ['child_a_enrol_schedule1',
                       'child_b_enrol_schedule1',
                       'child_c_enrol_schedule1',
                       'child_a_sec_schedule1',
                       'child_b_sec_schedule1',
                       'child_c_sec_schedule1']

    conditional_fieldlists = {}

    for schedule in schedules:
        conditional_fieldlists.update({schedule: (Insert(
            'last_att_sche_visit', 'infant_feeding_changed',
            after='report_datetime'),
            Insert(
            'child_weaned',
            after='continuing_to_bf'),
            Insert(
            'formula_first_report',
            after='took_formula'))
            })

    def get_fieldsets(self, request, obj=None):
        """Returns fieldsets after modifications declared in
        "conditional" dictionaries.
        """
        fieldsets = super().get_fieldsets(request, obj=obj)
        fieldsets = Fieldsets(fieldsets=fieldsets)
        key = self.get_key(request, obj)

        fieldset = self.conditional_fieldsets.get(key)

        if fieldset:
            try:
                fieldset = tuple(fieldset)
            except TypeError:
                fieldset = (fieldset,)
            for f in fieldset:
                fieldsets.add_fieldset(fieldset=f)

        fieldlist = self.conditional_fieldlists.get(key)
        if fieldlist:

            for fl in fieldlist:
                try:
                    fieldsets.insert_fields(
                        *fl.insert_fields,
                        insert_after=fl.insert_after,
                        section=fl.section)
                except AttributeError:
                    pass
                try:
                    fieldsets.remove_fields(
                        *fl.remove_fields,
                        section=fl.section)
                except AttributeError:
                    pass

        fieldsets = self.update_fieldset_for_form(
            fieldsets, request)
        fieldsets.move_to_end(self.fieldsets_move_to_end)
        return fieldsets.fieldsets

    def is_preg_enroll_quart(self, appt):

        try:
            Appointment.objects.get(subject_identifier=appt.subject_identifier,
                                    visit_code='2000D')
        except Appointment.DoesNotExist:
            return False
        else:
            return True

    def get_key(self, request, obj=None):

        schedule_name = None

        if self.get_previous_instance(request):
            try:
                model_obj = self.get_instance(request)
            except ObjectDoesNotExist:
                schedule_name = None
            else:
                schedule_name = model_obj.schedule_name

                if 'child_a_quart' in schedule_name:
                    if self.is_preg_enroll_quart(model_obj):
                        return schedule_name
                    return None

        return schedule_name

    def get_form(self, request, obj=None, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        form.previous_instance = self.get_previous_instance(request)
        return form
