from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_child_admin
from ..forms import TbRoutineScreenAdolForm
from ..models import TbRoutineScreenAdol
from .model_admin_mixins import ChildCrfModelAdminMixin


@admin.register(TbRoutineScreenAdol, site=flourish_child_admin)
class TbRoutineScreenAdolAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    form = TbRoutineScreenAdolForm
