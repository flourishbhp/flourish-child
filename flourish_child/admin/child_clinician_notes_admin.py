from django.contrib import admin
from edc_model_admin import TabularInlineMixin
from edc_odk.admin import StampImageActionMixin

from ..admin_site import flourish_child_admin
from ..forms import ChildClinicianNotesForm, ClinicianNotesImageForm
from ..models import ChildClinicianNotes, ClinicianNotesImage
from .model_admin_mixins import ChildCrfModelAdminMixin


class ClinicianNotesImageInline(TabularInlineMixin, admin.TabularInline):

    model = ClinicianNotesImage
    form = ClinicianNotesImageForm
    extra = 0

    fields = ('clinician_notes_image', 'image', 'user_uploaded', 'datetime_captured',
              'modified', 'hostname_created',)

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        fields = ('clinician_notes_image', 'datetime_captured',
                  'user_uploaded') + fields

        return fields


@admin.register(ChildClinicianNotes, site=flourish_child_admin)
class ClinicianNotesAdmin(StampImageActionMixin, ChildCrfModelAdminMixin,
                          admin.ModelAdmin):

    form = ChildClinicianNotesForm

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
            ]}
         ), )

    inlines = [ClinicianNotesImageInline]
