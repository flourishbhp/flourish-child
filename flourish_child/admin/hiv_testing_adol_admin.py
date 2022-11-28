from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import HIVTestingAdolForm
from ..models import HivTestingAdol


@admin.register(HivTestingAdol, site=flourish_child_admin)
class HivTestingAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    form = HIVTestingAdolForm
