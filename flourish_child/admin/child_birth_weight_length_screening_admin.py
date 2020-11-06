from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import ChildBirthScreeningForm
from ..models import ChildBirthScreening


@admin.register(ChildBirthScreening, site=flourish_child_admin)
class ChildBirthScreeningAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = ChildBirthScreeningForm

    fieldsets = (
        (None, {
            'fields': (
                'weight',
                'length',
                'gestational_age',
                'arv_exposure')
        }), audit_fieldset_tuple
    )
