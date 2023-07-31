from flourish_child.choices import HIGHEST_EDUCATION
from itertools import chain

from django import forms
from django.apps import apps as django_apps
from django.db.models import ManyToManyField
from edc_constants.constants import NO, YES

from flourish_child_validations.form_validators import AcademicPerformanceFormValidator

from ..models import AcademicPerformance
from .child_form_mixin import ChildModelFormMixin


class AcademicPerformanceForm(ChildModelFormMixin):

    form_validator_cls = AcademicPerformanceFormValidator

    child_socio_demographic_model = 'flourish_child.childsociodemographic'

    education_level = forms.ChoiceField(
        label='What level/class of school is the child currently in?',
        disabled=True,
        choices=HIGHEST_EDUCATION)

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop("initial", {})
        instance = kwargs.get("instance")
        previous_instance = getattr(self, "previous_instance", None)

        # child visit is only available onload page other None
        # args is prepolated only on save otherwise None
        child_visit_id = initial.get(
            'child_visit', args[0]['child_visit'] if args else None)

        try:
            child_visit_obj = self.visit_model.objects.get(id=child_visit_id)
        except self.visit_model.DoesNotExist:
            child_visit_obj = None

        if not instance and previous_instance:
            for key in self.base_fields.keys():
                if key not in ["child_visit", "report_datetime", "education_level"]:
                    initial[key] = getattr(previous_instance, key)

        if child_visit_obj:

            child_education_level = self.child_social_education_level(
                child_visit=child_visit_obj)

            # get the education_level from child socio demographics in the same visit
            # regard less of the previous education level of the previous instance
            # check if child_visit_id not null to avoid exceptions then initialize
            # education_level taken from child socio demographics in the same visit
            initial['education_level'] = child_education_level

        kwargs['initial'] = initial

        super().__init__(*args, **kwargs)

    @property
    def child_socio_demographic_cls(self):
        return django_apps.get_model(self.child_socio_demographic_model)

    def child_social_education_level(self, child_visit):
        """
        Get the child demographics from the same visit
        """

        try:
            child_socio_demographic = self.child_socio_demographic_cls.objects.get(
                child_visit=child_visit)
        except self.child_socio_demographic_cls.DoesNotExist:
            try:
                child_socio_demographic = self.child_socio_demographic_cls.objects.filter(
                    child_visit__subject_identifier=child_visit.subject_identifier,
                    report_datetime__lte=child_visit.report_datetime).latest('report_datetime')
            except self.child_socio_demographic_cls.DoesNotExist:
                return None
        return child_socio_demographic.education_level

    def clean(self):
        previous_instance = getattr(self, 'previous_instance', None)

        self.validate_prev_results_pending(previous_instance)

        has_changed = self.compare_instance_fields(previous_instance)

        academic_perf_changed = self.cleaned_data.get('academic_perf_changed')

        child_visit = self.cleaned_data.get('child_visit')

        if academic_perf_changed:
            if academic_perf_changed == YES and not has_changed:
                message = {
                    "academic_perf_changed": ("Participant's academic performance information "
                                              "has not changed since last visit. Please update"
                                              " the information on this form.")
                }
                raise forms.ValidationError(message)
            elif academic_perf_changed == NO and has_changed:
                message = {
                    "academic_perf_changed": ("Participant's academic performance information "
                                              "has been changed in this CRF since last visit."
                                              " The answer should be yes")
                }
                raise forms.ValidationError(message)

        try:
            self.child_socio_demographic_cls.objects.get(
                child_visit=child_visit)
        except self.child_socio_demographic_cls.DoesNotExist:
            message = {
                    "education_level": ("Participant's socio demographic information "
                                        "is missing. Kindly complete the form first.")
                }
            raise forms.ValidationError(message)

        cleaned_data = super().clean()
        return cleaned_data

    def validate_prev_results_pending(self, prev_instance):
        overall_performance = getattr(prev_instance, 'overall_performance', None)
        child_visit = getattr(prev_instance, 'child_visit', None)
        if overall_performance == 'pending':
            message = {'__all__':
                       'Overall performance results is still pending from the '
                       f'last visit {child_visit.visit_code}. Cannot capture'
                       ' academic performance until results captured at previous visit.'}
            raise forms.ValidationError(message)

    def compare_instance_fields(self, prev_instance=None):
        exclude_fields = [
            "modified",
            "created",
            "user_created",
            "user_modified",
            "hostname_created",
            "hostname_modified",
            "device_created",
            "device_modified",
            "report_datetime",
            "child_visit",
            "academic_perf_changed",
        ]

        # self.data was replaced because clean_data already contain
        # clean_data is alreadu populated when used under clean

        if prev_instance:
            other_values = self.model_to_dict(
                prev_instance, exclude=exclude_fields)
            values = {
                key: self.cleaned_data.get(key, "not_taking_subject")
                for key in other_values.keys()
            }
            if self.cleaned_data.get("grade_points") == "":
                values["grade_points"] = None
            values["education_level_other"] = self.cleaned_data.get(
                "education_level_other")
            if values.get("grade_points"):
                values["grade_points"] = int(values.get("grade_points"))
            return values != other_values
        return False

    def model_to_dict(self, instance, exclude):
        opts = instance._meta
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
            if not getattr(f, "editable", False):
                continue
            if exclude and f.name in exclude:
                continue
            if isinstance(f, ManyToManyField):
                data[f.name] = [str(obj.id)
                                for obj in f.value_from_object(instance)]
                continue
            data[f.name] = f.value_from_object(instance) or None
        return data

    class Meta:
        model = AcademicPerformance
        fields = "__all__"
