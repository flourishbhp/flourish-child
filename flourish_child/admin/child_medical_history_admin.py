from django.contrib import admin
from edc_fieldsets.fieldlist import Insert
from edc_fieldsets.fieldsets_modeladmin_mixin import FormLabel
from edc_model_admin import audit_fieldset_tuple
from edc_fieldsets.fieldsets import Fieldsets
from django.core.exceptions import ObjectDoesNotExist
from django.apps import apps as django_apps
from edc_fieldsets.fieldsets import Fieldsets
from edc_base.utils import age
from edc_constants.constants import FEMALE

from ..admin_site import flourish_child_admin
from ..forms import ChildMedicalHistoryForm
from ..models import ChildMedicalHistory
from .model_admin_mixins import ChildCrfModelAdminMixin


@admin.register(ChildMedicalHistory, site=flourish_child_admin)
class ChildMedicalHistoryAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = ChildMedicalHistoryForm

    list_display = ("child_visit", "chronic_since")
    list_filter = ("chronic_since",)

    fieldsets = (
        (
            None,
            {
                "fields": [
                    "child_visit",
                    "report_datetime",
                    "current_hiv_status",
                    "chronic_since",
                    "child_chronic",
                    "child_chronic_other",
                ]
            },
        ),
        audit_fieldset_tuple,
    )

    radio_fields = {
        "chronic_since": admin.VERTICAL,
        "med_history_changed": admin.VERTICAL,
        "current_hiv_status": admin.VERTICAL,
        "preg_test_performed": admin.VERTICAL,
        "pregnancy_test_result": admin.VERTICAL,
        "is_lmp_date_estimated": admin.VERTICAL,
    }

    filter_horizontal = ("child_chronic",)

    custom_form_labels = [
        FormLabel(
            field="med_history_changed",
            label=(
                "Since the last scheduled visit in {previous}, has any of "
                "your medical history changed?"
            ),
            previous_appointment=True,
        )
    ]

    conditional_fieldlists = {
        "child_a_sec_qt_schedule1": Insert(
            "med_history_changed", after="report_datetime"
        ),
        "child_a_quart_schedule1": Insert(
            "med_history_changed", after="report_datetime"
        ),
        "child_b_sec_qt_schedule1": Insert(
            "med_history_changed", after="report_datetime"
        ),
        "child_b_quart_schedule1": Insert(
            "med_history_changed", after="report_datetime"
        ),
        "child_c_sec_qt_schedule1": Insert(
            "med_history_changed", after="report_datetime"
        ),
        "child_c_quart_schedule1": Insert(
            "med_history_changed", after="report_datetime"
        ),
        "child_pool_schedule1": Insert("med_history_changed", after="report_datetime"),
        
        "female_above_12": Insert(
            "preg_test_performed",
            "pregnancy_test_result",
            "last_menstrual_period",
            "is_lmp_date_estimated",
            after="current_hiv_status",
        ),
    }
    
    def get_fieldsets(self, request, obj=None):
        """Returns fieldsets after modifications declared in
        "conditional" dictionaries.
        """
        fieldsets = super().get_fieldsets(request, obj=obj)
        fieldsets = Fieldsets(fieldsets=fieldsets)
        
        keys = self.get_keys(request, obj)
        for key in keys:
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
                try:
                    fieldsets.insert_fields(
                        *fieldlist.insert_fields,
                        insert_after=fieldlist.insert_after,
                        section=fieldlist.section)
                except AttributeError:
                    pass
                try:
                    fieldsets.remove_fields(
                        *fieldlist.remove_fields,
                        section=fieldlist.section)
                except AttributeError:
                    pass
        fieldsets = self.update_fieldset_for_form(
            fieldsets, request)
        fieldsets.move_to_end(self.fieldsets_move_to_end)
        return fieldsets.fieldsets
    
    def get_key(self, request, obj=None):
        pass

    
    def get_keys(self, request, obj=None):
        result = self.get_is_female_and_above12(request)

        keys = []
        if self.get_previous_instance(request):
            try:
                model_obj = self.get_instance(request)
            except ObjectDoesNotExist:
                pass
            else:
                schedule_name = model_obj.schedule_name
                keys.append(schedule_name)

        if result == 'female_above_12':
            keys.append('female_above_12')
        return keys   

    def get_is_female_and_above12(self, request, obj=None):
        subject_consent_cls = django_apps.get_model(
            'flourish_child.childassent')
        try:
            consent_obj = subject_consent_cls.objects.get(
                subject_identifier=request.GET.get('subject_identifier'))
        except subject_consent_cls.DoesNotExist:
            pass
        else:
            try:
                visit_obj = self.visit_model.objects.get(
                    id=request.GET.get('child_visit'))
            except self.visit_model.DoesNotExist:
                pass
            else:
                if age(consent_obj.dob, visit_obj.report_datetime).years >= 12 and consent_obj.gender == FEMALE:
                    return 'female_above_12'

    def get_form(self, request, obj=None, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        form.previous_instance = self.get_previous_instance(request)
        return form
