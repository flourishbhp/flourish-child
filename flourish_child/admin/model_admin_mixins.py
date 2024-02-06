import datetime

from django.apps import apps as django_apps
from django.conf import settings
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils import timezone
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_base.sites.admin import ModelAdminSiteMixin
from edc_fieldsets import FieldsetsModelAdminMixin
from edc_metadata import NextFormGetter
from edc_model_admin import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin,
    ModelAdminReadOnlyMixin, ModelAdminInstitutionMixin,
    FormAsJSONModelAdminMixin, ModelAdminRedirectOnDeleteMixin)
from edc_visit_tracking.modeladmin_mixins import (
    CrfModelAdminMixin as VisitTrackingCrfModelAdminMixin)
from simple_history.admin import SimpleHistoryAdmin

from .exportaction_mixin import ExportActionMixin
from ..helper_classes.utils import child_utils


class ModelAdminMixin(ModelAdminNextUrlRedirectMixin,
                      ModelAdminFormInstructionsMixin,
                      ModelAdminFormAutoNumberMixin, ModelAdminRevisionMixin,
                      ModelAdminAuditFieldsMixin, ModelAdminReadOnlyMixin,
                      ModelAdminInstitutionMixin,
                      ModelAdminRedirectOnDeleteMixin,
                      ModelAdminSiteMixin,
                      ExportActionMixin):

    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'
    next_form_getter_cls = NextFormGetter


class ExportRequisitionCsvMixin:

    def fix_date_format(self, obj_dict=None):
        """Change all dates into a format for the export
        and split the time into a separate value.

        Format: m/d/y
        """

        result_dict_obj = {**obj_dict}
        for key, value in obj_dict.items():
            if isinstance(value, datetime.datetime):
                value = timezone.make_naive(value)
                time_value = value.time()
                time_variable = key + '_time'
                result_dict_obj[key] = value.date()
                result_dict_obj[time_variable] = time_value
        return result_dict_obj

    def export_as_csv(self, request, queryset):
        records = []
        for obj in queryset:
            obj_data = self.fix_date_format(obj.__dict__.copy())
            obj_data.update(panel_name=obj.panel.name)
            records.append(obj_data)

        # Inherinted from the Admin Export Helper on the parent export mixin
        response = self.write_to_excel(records)
        return response

    export_as_csv.short_description = "Export with panel name"


class ChildCrfModelAdminMixin(
        VisitTrackingCrfModelAdminMixin, ModelAdminMixin,
        FieldsetsModelAdminMixin, FormAsJSONModelAdminMixin,
        SimpleHistoryAdmin, admin.ModelAdmin):

    show_save_next = True
    show_cancel = True
    appointment_model = 'flourish_child.appointment'

    post_url_on_delete_name = settings.DASHBOARD_URL_NAMES.get(
        'child_dashboard_url')

    @property
    def cohort_schedules_cls(self):
        model_name = 'flourish_caregiver.cohortschedules'
        return django_apps.get_model(model_name)

    def post_url_on_delete_kwargs(self, request, obj):
        return dict(
            subject_identifier=obj.child_visit.subject_identifier,
            appointment=str(obj.child_visit.appointment.id))

    def view_on_site(self, obj):
        dashboard_url_name = settings.DASHBOARD_URL_NAMES.get(
            'child_dashboard_url')
        try:
            url = reverse(
                dashboard_url_name, kwargs=dict(
                    subject_identifier=obj.child_visit.subject_identifier,
                    appointment=str(obj.child_visit.appointment.id)))
        except NoReverseMatch:
            url = super().view_on_site(obj)
        return url

    def get_appointment(self, request):
        """Returns the appointment instance for this request or None.
        """
        appointment_model_cls = django_apps.get_model(self.appointment_model)
        return appointment_model_cls.objects.get(
            pk=request.GET.get('appointment'))
        return None

    def get_previous_instance(self, request, instance=None, **kwargs):
        """Returns a model instance that is the first occurrence of a previous
        instance relative to this object's appointment.
        """
        obj = None
        appointment = instance or self.get_instance(request)

        if appointment:
            while appointment:
                options = {
                    '{}__appointment'.format(self.model.visit_model_attr()):
                    child_utils.get_previous_appt_instance(appointment)}
                try:
                    obj = self.model.objects.get(**options)
                except ObjectDoesNotExist:
                    pass
                else:
                    break
                appointment = child_utils.get_previous_appt_instance(appointment)
        return obj

    def get_instance(self, request):
        try:
            appointment = self.get_appointment(request)
        except ObjectDoesNotExist:
            return None
        else:
            return appointment

    def get_key(self, request, obj=None):

        schedule_name = None

        if self.get_previous_instance(request):
            try:
                model_obj = self.get_instance(request)
            except ObjectDoesNotExist:
                schedule_name = None
            else:
                schedule_name = model_obj.schedule_name
        return schedule_name
