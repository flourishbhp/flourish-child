from django.contrib import admin
from edc_fieldsets.fieldlist import Insert
from edc_fieldsets.fieldsets_modeladmin_mixin import FormLabel
from edc_model_admin import audit_fieldset_tuple


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
                    "chronic_since",
                    "child_chronic",
                    "child_chronic_other",
                    "current_hiv_status",
                ]
            },
        ),
        audit_fieldset_tuple,
    )

    radio_fields = {
        "chronic_since": admin.VERTICAL,
        "med_history_changed": admin.VERTICAL,
        "current_hiv_status": admin.VERTICAL,
        "is_pregnant": admin.VERTICAL,
        "is_lmp_date_estimated": admin.VERTICAL,
        "pregnancy_test_result": admin.VERTICAL,
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
            "med_history_changed",
            "is_pregnant",
            "last_menstrual_period",
            "is_lmp_date_estimated",
            "pregnancy_test_result",
            after="report_datetime",
        ),
    }

    def get_fieldsets(self, request, obj=None):
        return self.get_fieldsets_update(request, obj)

    def get_form(self, request, obj=None, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        form.previous_instance = self.get_previous_instance(request)
        return form
