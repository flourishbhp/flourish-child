from django.contrib import admin
from edc_senaite_interface.admin import SenaiteResultAdminMixin

from ..admin_site import flourish_child_admin
from ..forms import ChildRequisitionResultForm
from ..models import ChildRequisitionResult


@admin.register(ChildRequisitionResult, site=flourish_child_admin)
class ChildRequisitionResultAdmin(SenaiteResultAdminMixin, admin.ModelAdmin):

    form = ChildRequisitionResultForm
