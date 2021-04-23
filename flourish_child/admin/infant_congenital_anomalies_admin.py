from .model_admin_mixins import ModelAdminMixin
from ..models.infant_congenital_anomalies import InfantTrisomies

from django.contrib import admin
from edc_model_admin import TabularInlineMixin
from edc_model_admin.model_admin_audit_fields_mixin import audit_fieldset_tuple

from ..admin_site import flourish_child_admin
from ..constants import INFANT
from ..forms import (
    InfantCongenitalAnomaliesForm, InfantFacialDefectForm,
    InfantCleftDisorderForm, InfantMouthUpGiForm,
    InfantCardioDisorderForm,
    InfantRespiratoryDefectForm, InfantLowerGiForm,
    InfantFemaleGenitalForm,
    InfantMaleGenitalForm, InfantRenalForm,
    InfantMusculoskeletalForm,
    InfantSkinForm, InfantTrisomiesForm,
    InfantCnsForm
)
from ..models import (
    InfantCongenitalAnomalies, InfantCns, InfantFacialDefect,
    InfantCleftDisorder, InfantMouthUpGi, InfantCardioDisorder,
    InfantRespiratoryDefect, InfantLowerGi, InfantMaleGenital,
    InfantFemaleGenital, InfantRenal, InfantMusculoskeletal,
    InfantSkin
)
from .model_admin_mixins import ChildCrfModelAdminMixin


class InfantCnsInline(TabularInlineMixin, admin.TabularInline):

    model = InfantCns
    form = InfantCnsForm
    extra = 0

    fieldsets = (
        ['Infant Congenital Anomalies', {
            'fields': (
                'congenital_anomalies',
                'cns',
                'abnormality_status',
                'cns_other',)},
         ], audit_fieldset_tuple)


class InfantFacialDefectInline(TabularInlineMixin, admin.TabularInline):

    model = InfantFacialDefect
    form = InfantFacialDefectForm
    extra = 0

    fieldsets = (
        ['Infant Facial Defect', {
            'fields': (
                'congenital_anomalies',
                'facial_defect',
                'abnormality_status',
                'facial_defects_other',)},
         ], audit_fieldset_tuple)


class InfantCleftDisorderInline(TabularInlineMixin, admin.TabularInline):

    model = InfantCleftDisorder
    form = InfantCleftDisorderForm
    extra = 0

    fieldsets = (
        ['Infant Clef Disorder', {
            'fields': (
                'congenital_anomalies',
                'cleft_disorder',
                'abnormality_status',
                'cleft_disorders_other',)},
         ],)


class InfantMouthUpGiInline(TabularInlineMixin, admin.TabularInline):

    model = InfantMouthUpGi
    form = InfantMouthUpGiForm
    extra = 0

    fieldsets = (
        ['Infant Mouth Up', {
            'fields': (
                'congenital_anomalies',
                'mouth_up_gi',
                'abnormality_status',
                'mouth_up_gi_other',)},
         ], audit_fieldset_tuple)


class InfantCardioDisorderInline(TabularInlineMixin, admin.TabularInline):

    model = InfantCardioDisorder
    form = InfantCardioDisorderForm
    extra = 0

    fieldsets = (
        ['Infant Cardio Disorder', {
            'fields': (
                'congenital_anomalies',
                'cardio_disorder',
                'abnormality_status',
                'cardiovascular_other',)},
         ], audit_fieldset_tuple)


class InfantRespiratoryDefectInline(TabularInlineMixin, admin.TabularInline):

    model = InfantRespiratoryDefect
    form = InfantRespiratoryDefectForm
    extra = 0

    fieldsets = (
        ['Infant Respiratory Defect', {
            'fields': (
                'congenital_anomalies',
                'respiratory_defect',
                'abnormality_status',
                'respiratory_defects_other',)},
         ], audit_fieldset_tuple)


class InfantLowerGiInline(TabularInlineMixin, admin.TabularInline):

    model = InfantLowerGi
    form = InfantLowerGiForm
    extra = 0

    fieldsets = (
        ['Infant Lower Gi', {
            'fields': (
                'congenital_anomalies',
                'lower_gi',
                'abnormality_status',
                'lower_gi_other',)},
         ], audit_fieldset_tuple)


class InfantFemaleGenitalInline(TabularInlineMixin, admin.TabularInline):

    model = InfantFemaleGenital
    form = InfantFemaleGenitalForm
    extra = 0

    fieldsets = (
        ['Infant Female Genital', {
            'fields': (
                'congenital_anomalies',
                'female_genital',
                'abnormality_status',
                'female_genital_other',)},
         ], audit_fieldset_tuple)


class InfantMaleGenitalInline(TabularInlineMixin, admin.TabularInline):

    model = InfantMaleGenital
    form = InfantMaleGenitalForm
    extra = 0

    fieldsets = (
        ['Infant Male Genital', {
            'fields': (
                'congenital_anomalies',
                'male_genital',
                'abnormality_status',
                'male_genital_other',)},
         ], audit_fieldset_tuple)


class InfantRenalInline(TabularInlineMixin, admin.TabularInline):

    model = InfantRenal
    form = InfantRenalForm
    extra = 0

    fieldsets = (
        ['Infant Renal', {
            'fields': (
                'congenital_anomalies',
                'renal',
                'abnormality_status',
                'renal_other',)},
         ], audit_fieldset_tuple)


class InfantMusculoskeletalInline(TabularInlineMixin, admin.TabularInline):

    model = InfantMusculoskeletal
    form = InfantMusculoskeletalForm
    extra = 0

    fieldsets = (
        ['Infant Musculo skeletal', {
            'fields': (
                'congenital_anomalies',
                'musculo_skeletal',
                'abnormality_status',
                'musculo_skeletal_other',)},
         ], audit_fieldset_tuple)


class InfantSkinInline(TabularInlineMixin, admin.TabularInline):

    model = InfantSkin
    form = InfantSkinForm
    extra = 0

    fieldsets = (
        ['Infant Skin', {
            'fields': (
                'congenital_anomalies',
                'skin',
                'abnormality_status',
                'skin_other',)},
         ], audit_fieldset_tuple)


class InfantTrisomiesInline(TabularInlineMixin, admin.TabularInline):

    model = InfantTrisomies
    form = InfantTrisomiesForm
    extra = 0

    fieldsets = (
        ['Infant Trisomies', {
            'fields': (
                'congenital_anomalies',
                'trisomies',
                'abnormality_status',
                'trisomies_other',)},
         ], audit_fieldset_tuple)


@admin.register(InfantCongenitalAnomalies, site=flourish_child_admin)
class InfantCongenitalAnomaliesAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = InfantCongenitalAnomaliesForm

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
            ]
        }

        ),
    )

    dashboard_type = INFANT
    visit_model_name = 'infantvisit'

    list_display = ('child_visit',)

    inlines = [
        InfantCnsInline,
        InfantFacialDefectInline,
        InfantCleftDisorderInline,
        InfantMouthUpGiInline,
        InfantCardioDisorderInline,
        InfantRespiratoryDefectInline,
        InfantLowerGiInline,
        InfantFemaleGenitalInline,
        InfantMaleGenitalInline,
        InfantRenalInline,
        InfantMusculoskeletalInline,
        InfantSkinInline,
        InfantTrisomiesInline]


@admin.register(InfantCns, site=flourish_child_admin)
class InfantCnsAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = InfantCnsForm

    fieldsets = (
        (None, {
            'fields': [
                'congenital_anomalies',
                'cns',
                'abnormality_status',
                'cns_other',
            ]
        }

        ), audit_fieldset_tuple,
    )

    list_display = ('congenital_anomalies', 'abnormality_status',)

    list_filter = ('cns',)

    radio_fields = {
        'cns': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL}


@admin.register(InfantFacialDefect, site=flourish_child_admin)
class InfantFacialDefectAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = InfantFacialDefectForm

    fieldsets = (
        (None, {
            'fields': [
                'congenital_anomalies',
                'facial_defect',
                'abnormality_status',
                'facial_defects_other',
            ]
        }

        ), audit_fieldset_tuple,
    )
    list_display = ('congenital_anomalies',)

    search_fields = [
        'congenital_anomalies__child_visit__appointment__subject_identifier',
        'congenital_anomalies__child_visit__appointment__initials', ]

    radio_fields = {
        'facial_defect': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }


@admin.register(InfantCleftDisorder, site=flourish_child_admin)
class InfantCleftDisorderAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = InfantCleftDisorderForm

    fieldsets = (
        (None, {
            'fields': [
                'congenital_anomalies',
                'cleft_disorder',
                'abnormality_status',
                'cleft_disorders_other',
            ]
        }

        ), audit_fieldset_tuple,
    )
    list_display = ('congenital_anomalies',)

    search_fields = [
        'congenital_anomalies__child_visit__appointment__subject_identifier',
        'congenital_anomalies__child_visit__appointment__initials', ]

    radio_fields = {
        'cleft_disorder': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }


@admin.register(InfantMouthUpGi, site=flourish_child_admin)
class InfantMouthUpGiAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = InfantMouthUpGiForm

    fieldsets = (
        (None, {
            'fields': [
                'congenital_anomalies',
                'mouth_up_gi',
                'abnormality_status',
                'mouth_up_gi_other',
            ]
        }

        ), audit_fieldset_tuple,
    )
    list_display = ('congenital_anomalies',)

    search_fields = [
        'congenital_anomalies__child_visit__appointment__subject_identifier',
        'congenital_anomalies__child_visit__appointment__initials', ]

    radio_fields = {
        'mouth_up_gi': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }


@admin.register(InfantCardioDisorder, site=flourish_child_admin)
class InfantCardioDisorderAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = InfantCardioDisorderForm

    fieldsets = (
        (None, {
            'fields': [
                'congenital_anomalies',
                'cardio_disorder',
                'abnormality_status',
                'cardiovascular_other',
            ]
        }

        ), audit_fieldset_tuple,
    )
    list_display = ('congenital_anomalies',)

    search_fields = [
        'congenital_anomalies__child_visit__appointment__subject_identifier',
        'congenital_anomalies__child_visit__appointment__initials', ]

    radio_fields = {
        'cardio_disorder': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }


@admin.register(InfantRespiratoryDefect, site=flourish_child_admin)
class InfantRespiratoryDefectAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = InfantRespiratoryDefectForm

    fieldsets = (
        (None, {
            'fields': [
                'congenital_anomalies',
                'respiratory_defect',
                'abnormality_status',
                'respiratory_defects_other',
            ]
        }

        ), audit_fieldset_tuple,
    )
    list_display = ('congenital_anomalies',)

    search_fields = [
        'congenital_anomalies__child_visit__appointment__subject_identifier',
        'congenital_anomalies__child_visit__appointment__initials', ]

    radio_fields = {
        'respiratory_defect': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }


@admin.register(InfantLowerGi, site=flourish_child_admin)
class InfantLowerGiAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = InfantLowerGiForm

    fieldsets = (
        (None, {
            'fields': [
                'congenital_anomalies',
                'lower_gi',
                'abnormality_status',
                'lower_gi_other',
            ]
        }

        ), audit_fieldset_tuple,
    )
    list_display = ('congenital_anomalies',)

    search_fields = [
        'congenital_anomalies__child_visit__appointment__subject_identifier',
        'congenital_anomalies__child_visit__appointment__initials', ]

    radio_fields = {
        'lower_gi': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }


@admin.register(InfantFemaleGenital, site=flourish_child_admin)
class InfantFemaleGenitalAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = InfantFemaleGenitalForm

    fieldsets = (
        (None, {
            'fields': [
                'congenital_anomalies',
                'female_genital',
                'abnormality_status',
                'female_genital_other',
            ]
        }

        ), audit_fieldset_tuple,
    )
    list_display = ('congenital_anomalies',)

    search_fields = [
        'congenital_anomalies__child_visit__appointment__subject_identifier',
        'congenital_anomalies__child_visit__appointment__initials', ]

    radio_fields = {
        'female_genital': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }


@admin.register(InfantMaleGenital, site=flourish_child_admin)
class InfantMaleGenitalAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = InfantMaleGenitalForm

    fieldsets = (
        (None, {
            'fields': [
                'congenital_anomalies',
                'male_genital',
                'abnormality_status',
                'male_genital_other',
            ]
        }

        ), audit_fieldset_tuple,
    )
    list_display = ('congenital_anomalies',)

    search_fields = [
        'congenital_anomalies__child_visit__appointment__subject_identifier',
        'congenital_anomalies__child_visit__appointment__initials', ]

    radio_fields = {
        'male_genital': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }


@admin.register(InfantRenal, site=flourish_child_admin)
class InfantRenalAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = InfantRenalForm

    fieldsets = (
        (None, {
            'fields': [
                'congenital_anomalies',
                'renal',
                'abnormality_status',
                'renal_other',
            ]
        }

        ), audit_fieldset_tuple,
    )
    list_display = ('congenital_anomalies',)

    search_fields = [
        'congenital_anomalies__child_visit__appointment__subject_identifier',
        'congenital_anomalies__child_visit__appointment__initials', ]

    radio_fields = {
        'renal': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }


@admin.register(InfantMusculoskeletal, site=flourish_child_admin)
class InfantMusculoskeletalAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = InfantMusculoskeletalForm

    fieldsets = (
        (None, {
            'fields': [
                'congenital_anomalies',
                'musculo_skeletal',
                'abnormality_status',
                'musculo_skeletal_other',
            ]
        }

        ), audit_fieldset_tuple,
    )
    list_display = ('congenital_anomalies',)

    search_fields = [
        'congenital_anomalies__child_visit__appointment__subject_identifier',
        'congenital_anomalies__child_visit__appointment__initials', ]

    radio_fields = {
        'musculo_skeletal': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }


@admin.register(InfantSkin, site=flourish_child_admin)
class InfantSkinAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = InfantSkinForm

    fieldsets = (
        (None, {
            'fields': [
                'congenital_anomalies',
                'skin',
                'abnormality_status',
                'skin_other',
            ]
        }

        ), audit_fieldset_tuple,
    )
    list_display = ('congenital_anomalies',)

    search_fields = [
        'congenital_anomalies__child_visit__appointment__subject_identifier',
        'congenital_anomalies__child_visit__appointment__initials', ]

    radio_fields = {
        'skin': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }


@admin.register(InfantTrisomies, site=flourish_child_admin)
class InfantTrisomiesAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = InfantTrisomiesForm

    fieldsets = (
        (None, {
            'fields': [
                'congenital_anomalies',
                'trisomies',
                'abnormality_status',
                'trisomies_other',
            ]
        }

        ), audit_fieldset_tuple,
    )
    list_display = ('congenital_anomalies',)

    search_fields = [
        'congenital_anomalies__child_visit__appointment__subject_identifier',
        'congenital_anomalies__child_visit__appointment__initials', ]

    radio_fields = {
        'trisomies': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }
