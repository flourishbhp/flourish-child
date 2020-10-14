from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import ChildBirthWeightLengthScreeningForm
from ..models import ChildBirthWeightLengthScreening


@admin.register(ChildBirthWeightLengthScreening, site=flourish_child_admin)
class ChildBirthWeightLengthScreeningAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = ChildBirthWeightLengthScreeningForm

    fieldsets = (
        (None, {
            'fields': (
                'weight',
                'length',
                'gestational_age',
                'arv_exposure')
        }), audit_fieldset_tuple
    )
