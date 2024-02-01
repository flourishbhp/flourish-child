from django.apps import apps as django_apps
from django.contrib import admin
from django.db.models import Q
from edc_fieldsets import Fieldlist
from edc_model_admin import StackedInlineMixin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_child_admin
from ..forms import ChildPreviousHospitalizationForm, ChildPreHospitalizationInlineForm
from ..models import ChildPreviousHospitalization, ChildPreHospitalizationInline
from .model_admin_mixins import ChildCrfModelAdminMixin


class ChildPreHospitalizationInlineAdmin(StackedInlineMixin, admin.StackedInline):
    model = ChildPreHospitalizationInline
    form = ChildPreHospitalizationInlineForm
    extra = 0

    fieldsets = (
        [None, {
            'fields': (
                'name_hospital',
                'name_hospital_other',
                'reason_hospitalized',
                'surgical_reason',
                'reason_hospitalized_other',
                'aprox_date',
                'date_estimated'
                )
            },
         ], audit_fieldset_tuple)

    radio_fields = {
        'name_hospital': admin.VERTICAL,
        'date_estimated': admin.VERTICAL,
        }

    filter_horizontal = ['reason_hospitalized']


@admin.register(ChildPreviousHospitalization, site=flourish_child_admin)
class ChildPreviousHospitalizationAdmin(ChildCrfModelAdminMixin,
                                        admin.ModelAdmin):
    form = ChildPreviousHospitalizationForm

    inlines = [ChildPreHospitalizationInlineAdmin, ]

    extra_context_models = ['childprehospitalizationInline']

    fieldsets = (
        (None, {
            'fields': (
                'child_visit',
                'report_datetime',
                'child_hospitalized',
                'hospitalized_count',
                )
            }
         ), audit_fieldset_tuple)

    radio_fields = {
        'child_hospitalized': admin.VERTICAL,
        'hos_last_visit': admin.VERTICAL,
        }

    def get_key(self, request, obj=None):
        schedule_name = super().get_key(request=request, obj=obj)
        if not schedule_name:
            model_obj = self.get_instance(request)
            schedule_name = model_obj.schedule_name if model_obj else None
        return schedule_name

    @property
    def quarterly_and_fu_schedules(self):
        schedules = self.cohort_schedules_cls.objects.filter(
            Q(schedule_type__icontains='quarterly') | Q(schedule_name__icontains='_fu_'),
            onschedule_model__startswith='flourish_child').values_list(
            'schedule_name', flat=True)
        return schedules

    @property
    def conditional_fieldlists(self):
        conditional_fieldlists = {}
        for schedule in self.quarterly_and_fu_schedules:
            conditional_fieldlists.update(
                {schedule: Fieldlist(remove_fields=('child_hospitalized',),
                                     insert_fields=('hos_last_visit',),
                                     insert_after=('report_datetime'))})
        return conditional_fieldlists

    def get_form(self, request, obj=None, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        form.previous_instance = self.get_previous_instance(request)
        return form

    def add_view(self, request, form_url='', extra_context=None):

        extra_context = extra_context or {}
        subject_identifier = request.GET.get('subject_identifier')
        child_visit = request.GET.get('child_visit')
        if self.extra_context_models:
            extra_context = self.get_model_data_per_visit(
                subject_identifier=subject_identifier, child_visit=child_visit)
        return super().add_view(
            request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):

        extra_context = extra_context or {}
        subject_identifier = request.GET.get('subject_identifier')
        child_visit = request.GET.get('child_visit')
        if self.extra_context_models:
            extra_context = self.get_model_data_per_visit(
                subject_identifier=subject_identifier, child_visit=child_visit)
        return super().change_view(
            request, object_id, form_url=form_url, extra_context=extra_context)

    def get_model_data_per_visit(self, subject_identifier=None, child_visit=None):

        model_dict = {}
        for model_name in self.extra_context_models:
            data_dict = {}
            model_cls = django_apps.get_model(f'flourish_child.{model_name}')
            model_objs = model_cls.objects.filter(
                child_pre_hospitalization__child_visit__subject_identifier=subject_identifier).exclude(
                child_pre_hospitalization__child_visit=child_visit)
            for model_obj in model_objs:
                visit_code = model_obj.visit.visit_code
                data_dict.setdefault(visit_code, [])
                data_dict[visit_code].append(model_obj)

            model_dict.update({model_name: data_dict})

        return model_dict
