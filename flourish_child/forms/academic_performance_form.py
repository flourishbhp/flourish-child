from itertools import chain

from django import forms
from django.db.models import ManyToManyField
from edc_constants.constants import NO, YES
from flourish_child_validations.form_validators import AcademicPerformanceFormValidator

from flourish_child.choices import HIGHEST_EDUCATION

from ..models import AcademicPerformance
from .child_form_mixin import ChildModelFormMixin


class AcademicPerformanceForm(ChildModelFormMixin):

    form_validator_cls = AcademicPerformanceFormValidator

    education_level = forms.CharField(
        disabled=True,
        label="What level/class of school is the child currently in?",
        widget=forms.Select(choices=HIGHEST_EDUCATION),
    )

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop("initial", {})
        instance = kwargs.get("instance")
        previous_instance = getattr(self, "previous_instance", None)

        if not instance and previous_instance:
            for key in self.base_fields.keys():
                if key not in ["child_visit", "report_datetime"]:
                    initial[key] = getattr(previous_instance, key)
        kwargs["initial"] = initial

        super().__init__(*args, **kwargs)

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
        if prev_instance:
            other_values = self.model_to_dict(prev_instance, exclude=exclude_fields)
            values = {
                key: self.data.get(key) or "not_taking_subject"
                for key in other_values.keys()
            }
            if self.data.get("grade_points") == "":
                values["grade_points"] = None
            values["education_level_other"] = self.data.get("education_level_other")
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
                data[f.name] = [str(obj.id) for obj in f.value_from_object(instance)]
                continue
            data[f.name] = f.value_from_object(instance) or None
        return data

    class Meta:
        model = AcademicPerformance
        fields = "__all__"
