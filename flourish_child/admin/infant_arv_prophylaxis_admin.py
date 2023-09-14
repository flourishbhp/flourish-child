from django.contrib import admin

from edc_model_admin import TabularInlineMixin, audit_fieldset_tuple

from ..admin_site import flourish_child_admin
from ..forms import InfantArvProphylaxisForm, ChildArvProphDatesForm
from ..models import InfantArvProphylaxis, ChildArvProphDates
from .model_admin_mixins import ChildCrfModelAdminMixin


class ChildArvProphDatesInlineAdmin(TabularInlineMixin, admin.TabularInline):
    model = ChildArvProphDates
    form = ChildArvProphDatesForm
    extra = 0

    fieldsets = (
        (None, {
            'fields': (
                'arv_name',
                'arv_start_date',
                'arv_stop_date')
        }),
    )

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.request = request
        return formset


@admin.register(InfantArvProphylaxis, site=flourish_child_admin)
class InfantArvProphylaxisAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = InfantArvProphylaxisForm
    inlines = [ChildArvProphDatesInlineAdmin, ]

    fieldsets = (
        (None, {
            'fields': (
                'child_visit',
                'report_datetime',
                'took_art_proph',
                'reason_no_art',
                'reason_no_art_other',
                'art_status',
                'days_art_received',
                'reason_incomplete',
                'arvs_modified',
                'date_arvs_modified',
                'reason_modified',
                'specify_effects',
                'reason_modified_othr',
                'missed_dose',
                'missed_dose_count',
                'reason_missed', )
        }), audit_fieldset_tuple
    )

    radio_fields = {'took_art_proph': admin.VERTICAL,
                    'reason_no_art': admin.VERTICAL,
                    'art_status': admin.VERTICAL,
                    'arvs_modified': admin.VERTICAL,
                    'reason_modified': admin.VERTICAL,
                    'missed_dose': admin.VERTICAL, }

    list_display = ('child_visit', 'report_datetime', 'took_art_proph')

    list_filter = ('report_datetime', 'took_art_proph',)
