from itertools import chain

from django import forms
from django.apps import apps as django_apps
from django.db.models import ManyToManyField
from edc_constants.constants import NO, YES
from flourish_child_validations.form_validators import AcademicPerformanceFormValidator
from flourish_child.choices import HIGHEST_EDUCATION

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

        if not instance and previous_instance:
            for key in self.base_fields.keys():
                if key not in ["child_visit", "report_datetime", "education_level"]:
                    initial[key] = getattr(previous_instance, key)

        if child_visit_id:
            # get the education_level from child socio demographics in the same visit
            # regard less of the previous education level of the previous instance
            # check if child_visit_id not null to avoid exceptions
            # then initialize education_level taken from child socio demographics in the same visit
            initial['education_level'] = self.child_social_education_level(
                child_visit_id=child_visit_id)

        kwargs["initial"] = initial

        super().__init__(*args, **kwargs)

    @property
    def child_socio_demographic_cls(self):
        return django_apps.get_model(self.child_socio_demographic_model)

    def child_social_education_level(self, child_visit_id):
        """
        Get the child demographics from the same visit
        """
        child_socio_demographic = self.child_socio_demographic_cls.objects.get(
            child_visit_id=child_visit_id)
        return child_socio_demographic.education_level

    def clean(self):
        previous_instance = getattr(self, "previous_instance", None)
        has_changed = self.compare_instance_fields(previous_instance)
        
        academic_perf_changed = self.cleaned_data.get("academic_perf_changed")
        if academic_perf_changed:
            if academic_perf_changed == YES and not has_changed:
                message = {
                    "academic_perf_changed": "Participant's academic performance  information has changed since"
                    " last visit. Please update the information on this form."
                }
                raise forms.ValidationError(message)
            elif academic_perf_changed == NO and has_changed:
                message = {
                    "academic_perf_changed": "Participant's academic performance information has not changed "
                    "since last visit. Please don't make any changes to this form."
                }
                raise forms.ValidationError(message)
        cleaned_data = super().clean()
        return cleaned_data

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
                key: self.cleaned_data.get(key,  "not_taking_subject")
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
