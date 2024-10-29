from django.contrib import admin
from edc_fieldsets.fieldlist import Insert, Remove
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import ChildClinicalMeasurementsForm
from ..models import ChildClinicalMeasurements
from edc_fieldsets.fieldsets import Fieldsets
from edc_fieldsets.fieldset import Fieldset


@admin.register(ChildClinicalMeasurements, site=flourish_child_admin)
class ChildClinicalMeasurementsAdmin(ChildCrfModelAdminMixin,
                                     admin.ModelAdmin):
    form = ChildClinicalMeasurementsForm

    list_display = ('child_visit', 'child_weight_kg', 'child_height',
                    'child_systolic_bp', 'child_diastolic_bp',
                    'child_waist_circ',
                    'child_hip_circ')

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'is_child_preg',
                'child_weight_kg',
                'child_systolic_bp',
                'child_diastolic_bp',
                'child_height',
                'child_muac'
            ]},
         ),
        ('Child Waist and Hip Circumference', {
            'fields': [
                'child_waist_circ',
                'child_hip_circ',
            ]}
         ),
        audit_fieldset_tuple)

    radio_fields = {
        'is_child_preg': admin.VERTICAL,
        'visit_skin_fold_messure': admin.VERTICAL,
    }

    conditional_fieldlists = {}

    def get_key(self, request, obj=None):
        if obj:
            return obj.child_visit.visit_code
        else:
            appt_obj = self.get_instance(request)
            return appt_obj.visit_code if appt_obj else None

    followup_codes = ['3000', '3000A', '3000B', '3000C', '3000S']
    for fu_code in followup_codes:
        conditional_fieldlists.update(
            {fu_code: Insert('visit_skin_fold_messure',
                             after='child_hip_circ',
                             section='Child Waist and Hip Circumference'), })

    def get_fieldsets(self, request, obj=None):
        """ Conditionally add skin folds measurements only required for the
            FU appointments.
        """
        fieldsets = super().get_fieldsets(request, obj=obj)
        fieldsets = Fieldsets(fieldsets=fieldsets)

        skin_folds_fs = []
        _mapping = {
            'Skin Folds Triceps': ('skin_folds_triceps',
                                   'skin_folds_triceps_second',
                                   'skin_folds_triceps_third', ),

            'Skin Folds Subscapular': ('skin_folds_subscapular',
                                       'skin_folds_subscapular_second',
                                       'skin_folds_subscapular_third', ),

            'Skin Folds Suprailiac': ('skin_folds_suprailiac',
                                      'skin_folds_suprailiac_second',
                                      'skin_folds_suprailiac_third', ),
            }

        if self.get_key(request, obj) in self.followup_codes:
            for section, fields in _mapping.items():
                skin_folds_fs.append(Fieldset(*fields, section=section))

            fieldsets.add_fieldsets(skin_folds_fs)

            # Move audit fields to the bottom once skin folds sections
            # are added.
            fieldsets.move_to_end(sections=['Audit', ])

        return fieldsets.fieldsets
