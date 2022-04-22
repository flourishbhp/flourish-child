from django.apps import apps as django_apps
from django.conf import settings
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_base.sites.admin import ModelAdminSiteMixin
from edc_base.utils import age
from edc_constants.constants import FEMALE
from edc_fieldsets import FieldsetsModelAdminMixin
from edc_fieldsets.fieldsets import Fieldsets
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


class ChildCrfModelAdminMixin(
        VisitTrackingCrfModelAdminMixin, ModelAdminMixin,
        FieldsetsModelAdminMixin, FormAsJSONModelAdminMixin,
        SimpleHistoryAdmin, admin.ModelAdmin):

    show_save_next = True
    show_cancel = True
    appointment_model = 'flourish_child.appointment'

    post_url_on_delete_name = settings.DASHBOARD_URL_NAMES.get(
        'child_dashboard_url')

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
                    self.get_previous_appt_instance(appointment)}
                try:
                    obj = self.model.objects.get(**options)
                except ObjectDoesNotExist:
                    pass
                else:
                    break
                appointment = self.get_previous_appt_instance(appointment)
        return obj

    def get_previous_appt_instance(self, appointment):

        return appointment.__class__.objects.filter(
            subject_identifier=appointment.subject_identifier,
            timepoint__lt=appointment.timepoint,
            schedule_name__startswith=appointment.schedule_name[:7],
            visit_code_sequence=0).order_by('timepoint').last()

    def get_instance(self, request):
        try:
            appointment = self.get_appointment(request)
        except ObjectDoesNotExist:
            return None
        else:
            return appointment

    # def get_keys(self, request, obj=None):
        # result = self.get_is_female_and_above12(request)
        #
        # keys = []
        # if self.get_previous_instance(request):
            # try:
                # model_obj = self.get_instance(request)
            # except ObjectDoesNotExist:
                # pass
            # else:
                # schedule_name = model_obj.schedule_name
                # keys.append(schedule_name)
                #
        # if result == 'female_above_12':
            # keys.append('female_above_12')
        # return keys

    def get_key(self, request, obj=None):
        pass

    # def get_fieldsets_update(self, request, obj=None):
        # """Returns fieldsets after modifications declared in
        # "conditional" dictionaries.
        # """
        # fieldsets = super().get_fieldsets(request, obj=obj)
        # fieldsets = Fieldsets(fieldsets=fieldsets)
        # keys = self.get_keys(request, obj)
        # for key in keys:
            # fieldset = self.conditional_fieldsets.get(key)
            # if fieldset:
                # try:
                    # fieldset = tuple(fieldset)
                # except TypeError:
                    # fieldset = (fieldset,)
                # for f in fieldset:
                    # fieldsets.add_fieldset(fieldset=f)
            # fieldlist = self.conditional_fieldlists.get(key)
            # if fieldlist:
                # try:
                    # fieldsets.insert_fields(
                        # *fieldlist.insert_fields,
                        # insert_after=fieldlist.insert_after,
                        # section=fieldlist.section)
                # except AttributeError:
                    # pass
                # try:
                    # fieldsets.remove_fields(
                        # *fieldlist.remove_fields,
                        # section=fieldlist.section)
                # except AttributeError:
                    # pass
        # fieldsets = self.update_fieldset_for_form(
            # fieldsets, request)
        # fieldsets.move_to_end(self.fieldsets_move_to_end)
        # return fieldsets.fieldsets

    # def get_is_female_and_above12(self, request, obj=None):
        # subject_consent_cls = django_apps.get_model(
            # 'flourish_child.childassent')
        # try:
            # consent_obj = subject_consent_cls.objects.get(
                # subject_identifier=request.GET.get('subject_identifier'))
        # except subject_consent_cls.DoesNotExist:
            # pass
        # else:
            # try:
                # visit_obj = self.visit_model.objects.get(
                    # id=request.GET.get('child_visit'))
            # except self.visit_model.DoesNotExist:
                # pass
            # else:
                # if age(consent_obj.dob, visit_obj.report_datetime).years >= 12 and consent_obj.gender == FEMALE:
                    # return 'female_above_12'
