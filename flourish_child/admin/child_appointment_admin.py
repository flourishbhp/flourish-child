from edc_visit_schedule.fieldsets import visit_schedule_fieldset_tuple, visit_schedule_fields

from django.conf import settings
from django.contrib import admin
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.safestring import mark_safe
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_base.sites.admin import ModelAdminSiteMixin
from edc_model_admin import (
    ModelAdminFormInstructionsMixin, ModelAdminNextUrlRedirectMixin,
    ModelAdminFormAutoNumberMixin, ModelAdminRedirectOnDeleteMixin,
    ModelAdminAuditFieldsMixin, ModelAdminReadOnlyMixin,
    audit_fieldset_tuple)

from ..admin_site import flourish_child_admin
from ..forms import AppointmentForm
from ..models import Appointment
from .exportaction_mixin import ExportActionMixin


@admin.register(Appointment, site=flourish_child_admin)
class AppointmentAdmin(ModelAdminFormInstructionsMixin, ModelAdminNextUrlRedirectMixin,
                       ModelAdminFormAutoNumberMixin, ModelAdminRevisionMixin,
                       ModelAdminAuditFieldsMixin, ModelAdminRedirectOnDeleteMixin,
                       ModelAdminReadOnlyMixin, ModelAdminSiteMixin,
                       ExportActionMixin, admin.ModelAdmin):

    post_url_on_delete_name = settings.DASHBOARD_URL_NAMES.get(
        'child_dashboard_url')
    dashboard_url_name = settings.DASHBOARD_URL_NAMES.get(
        'child_dashboard_url')

    form = AppointmentForm
    date_hierarchy = 'appt_datetime'
    list_display = ('subject_identifier', '__str__',
                    'appt_datetime', 'appt_type', 'appt_status')
    list_filter = ('visit_code', 'appt_datetime', 'appt_type', 'appt_status')

    fieldsets = (
        (None, ({
            'fields': (
                'subject_identifier',
                'appt_datetime',
                'appt_type',
                'appt_status',
                'appt_reason',
                'comment')})),
        ('Timepoint', ({
            'classes': ('collapse',),
            'fields': (
                'timepoint',
                'timepoint_datetime',
                'visit_code_sequence',
                'facility_name')})),
        visit_schedule_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        'appt_type': admin.VERTICAL,
        'appt_status': admin.VERTICAL,
        'appt_reason': admin.VERTICAL
    }

    def post_url_on_delete_kwargs(self, request, obj):
        return dict(subject_identifier=obj.subject_identifier)

    def get_readonly_fields(self, request, obj=None):
        return (super().get_readonly_fields(request, obj=obj)
                +visit_schedule_fields
                +('subject_identifier', 'timepoint', 'timepoint_datetime',
                   'visit_code_sequence', 'facility_name'))

    def view_on_site(self, obj):
        try:
            url = reverse(
                self.dashboard_url_name, kwargs=dict(
                    subject_identifier=obj.subject_identifier))
        except NoReverseMatch:
            url = super().view_on_site(obj)
        return url

    def change_view(self, request, object_id, form_url='', extra_context=None):

        extra_context = extra_context or {}
        app_obj = Appointment.objects.get(id=object_id)

        earliest_start = (app_obj.timepoint_datetime -
                          app_obj.visits.get(app_obj.visit_code).rlower)

        latest_start = (app_obj.timepoint_datetime +
                        app_obj.visits.get(app_obj.visit_code).rupper)

        ideal_start = app_obj.timepoint_datetime

        extra_context.update({'earliest_start': earliest_start.strftime("%Y-%m/%d, %H:%M:%S"),
                              'latest_start': latest_start.strftime("%Y-%m-%d, %H:%M:%S"),
                              'ideal_start': ideal_start.strftime("%Y-%m-%d, %H:%M:%S"), })

        return super().change_view(
            request, object_id, form_url=form_url, extra_context=extra_context)

    def update_change_instructions(self, extra_context):
        extra_context = extra_context or {}
        extra_context[
            'instructions'] = self.change_instructions or self.instructions

        earliest_start = extra_context.get('earliest_start')
        latest_start = extra_context.get('latest_start')
        ideal_start = extra_context.get('ideal_start')

        additional_instructions = mark_safe(
            '<table style="background-color: #f8f8f8;padding:10px;margin-top:10px;width:60%;'
            'border:0.5px solid #f0f0f0"><tr>'
            f'<td colspan="3">Earliest Start: <b>{earliest_start}</b></td>'
            f'<td colspan="3">Ideal Start: <b>{ideal_start}</b></td>'
            f'<td colspan="3">Latest Start: <b>{latest_start}</b></td>'
            '</table></tr> <BR>'
            'To start or continue to edit FORMS for this subject, change the '
            'appointment status below to "In Progress" and click SAVE. <BR>'
            '<i>Note: You may only edit one appointment at a time. '
            'Before you move to another appointment, change the appointment '
            'status below to "Incomplete or "Done".</i>')

        extra_context['additional_instructions'] = additional_instructions
        return extra_context
