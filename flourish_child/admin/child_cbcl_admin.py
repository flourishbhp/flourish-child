import json

from django.apps import apps as django_apps
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import ChildCBCLSection1Form, ChildCBCLSection2Form, ChildCBCLSection3Form, \
    ChildCBCLSection4Form
from ..models import ChildCBCLSection1, ChildCBCLSection2, ChildCBCLSection3, \
    ChildCBCLSection4
from ..helper_classes.utils import child_utils


@admin.register(ChildCBCLSection1, site=flourish_child_admin)
class ChildCBCLSection1Admin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    form = ChildCBCLSection1Form

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'acts_young',
                'unapproved_alc_intake',
                'alc_intake_desc',
                'argues_alot',
                'fails_to_finish',
                'enjoys_little',
                'bowel_incontinence',
                'bragging',
                'attention_deficit',
                'obssessive',
                'obssessive_desc',
                'hyperactive',
                'too_dependent',
                'feels_lonely',
                'confused',
                'cries_alot',
                'animal_cruelty',
                'bullies_other',
                'daydreams',
                'self_harms',
                'demands_attention',
                'destroys_belongings',
                'destroys_othr_things',
                'disobedient_home',
                'disobedient_school',
                'eating_problems',
                'unfitting',
                'unremorseful',
                'easily_jealous',
                'breaks_rules',
                'fearful',
                'fearful_desc',
                'fears_school',
            ]},),
        audit_fieldset_tuple)

    radio_fields = {'acts_young': admin.VERTICAL,
                    'unapproved_alc_intake': admin.VERTICAL,
                    'argues_alot': admin.VERTICAL,
                    'fails_to_finish': admin.VERTICAL,
                    'enjoys_little': admin.VERTICAL,
                    'bowel_incontinence': admin.VERTICAL,
                    'bragging': admin.VERTICAL,
                    'attention_deficit': admin.VERTICAL,
                    'obssessive': admin.VERTICAL,
                    'hyperactive': admin.VERTICAL,
                    'too_dependent': admin.VERTICAL,
                    'feels_lonely': admin.VERTICAL,
                    'confused': admin.VERTICAL,
                    'cries_alot': admin.VERTICAL,
                    'animal_cruelty': admin.VERTICAL,
                    'bullies_other': admin.VERTICAL,
                    'daydreams': admin.VERTICAL,
                    'self_harms': admin.VERTICAL,
                    'demands_attention': admin.VERTICAL,
                    'destroys_belongings': admin.VERTICAL,
                    'destroys_othr_things': admin.VERTICAL,
                    'disobedient_home': admin.VERTICAL,
                    'disobedient_school': admin.VERTICAL,
                    'eating_problems': admin.VERTICAL,
                    'unfitting': admin.VERTICAL,
                    'unremorseful': admin.VERTICAL,
                    'easily_jealous': admin.VERTICAL,
                    'breaks_rules': admin.VERTICAL,
                    'fearful': admin.VERTICAL,
                    'fears_school': admin.VERTICAL, }

    def export_as_csv(self, request, queryset):
        if request and request.POST.get('action', None) == 'export_as_csv':
            return super().export_as_csv(request, queryset)
        return self.export_combined_csv(request, queryset)

    def export_combined_csv(self, request, queryset):
        records = []
        combined_records = self.combine_crf_data(queryset)
        for record in combined_records:
            subject_identifier = record.get('childpid', None)
            caregiver_sid = child_utils.caregiver_subject_identifier(
                subject_identifier=subject_identifier)
            screening_identifier = self.screening_identifier(
                subject_identifier=caregiver_sid)
            previous_study = self.previous_bhp_study(
                subject_identifier=subject_identifier)
            study_maternal_identifier = self.study_maternal_identifier(
                    screening_identifier=screening_identifier)
            child_exposure_status = self.child_hiv_exposure(
                    study_maternal_identifier, study_maternal_identifier, caregiver_sid)

            enrol_cohort, current_cohort = self.get_cohort_details(subject_identifier)

            record.update(matpid=caregiver_sid,
                          old_matpid=study_maternal_identifier,
                          previous_study=previous_study,
                          child_exposure_status=child_exposure_status,
                          enrol_cohort=enrol_cohort,
                          current_cohort=current_cohort)

            # Exclude identifying values
            record = self.remove_exclude_fields(record)
            # Correct date formats
            record = self.fix_date_formats(record)
            records.append(record)

        response = self.write_to_csv(records)
        return response

    export_as_csv.short_description = _(
        'Export selected %(verbose_name_plural)s')

    actions = [export_as_csv]

    def combine_crf_data(self, queryset):
        """ Combine the CBCL crf forms data
        """
        combined_data = []
        crf_list = ['childcbclsection2', 'childcbclsection3', 'childcbclsection4']

        for crf_obj in queryset:
            visit = getattr(crf_obj, 'visit', None)

            data = dict(subject_identifier=getattr(visit, 'subject_identifier', None))
            # Update variable names for study identifiers
            data = self.update_variables(data)

            data.update(visit_code=getattr(visit, 'visit_code', None),
                        **crf_obj.__dict__.copy())

            visit_attr = crf_obj.visit_model_attr()

            for crf_name in crf_list:
                crf_cls = django_apps.get_model('flourish_child', crf_name)
                try:
                    obj = crf_cls.objects.get(**{f'{visit_attr}': visit})
                except crf_cls.DoesNotExist:
                    continue
                else:
                    combine_data = obj.__dict__.copy()
                    data.update(combine_data)
            combined_data.append(data)
        return combined_data


@admin.register(ChildCBCLSection2, site=flourish_child_admin)
class ChildCBCLSection2Admin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    form = ChildCBCLSection2Form

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'fear_harmful_thoughts',
                'fear_of_perfection',
                'feels_unloved',
                'feels_paranoia',
                'feels_worthless',
                'accident_prone',
                'fights_involvement',
                'teased_alot',
                'trouble_friends',
                'auditory_hallucination',
                'ah_desc',
                'impulsive',
                'loner',
                'cheating',
                'bites_nails',
                'nervousness',
                'nervous_moments',
                'nervous_desc',
                'nightmares',
                'disliked_by_othrs',
                'constipated',
                'anxiousness',
                'feels_dizzy',
                'feels_guity',
                'overeating',
                'overtired_noreason',
                'overweight', ]},),
        audit_fieldset_tuple)

    radio_fields = {'fear_harmful_thoughts': admin.VERTICAL,
                    'fear_of_perfection': admin.VERTICAL,
                    'feels_unloved': admin.VERTICAL,
                    'feels_paranoia': admin.VERTICAL,
                    'feels_worthless': admin.VERTICAL,
                    'accident_prone': admin.VERTICAL,
                    'fights_involvement': admin.VERTICAL,
                    'teased_alot': admin.VERTICAL,
                    'trouble_friends': admin.VERTICAL,
                    'auditory_hallucination': admin.VERTICAL,
                    'impulsive': admin.VERTICAL,
                    'loner': admin.VERTICAL,
                    'cheating': admin.VERTICAL,
                    'bites_nails': admin.VERTICAL,
                    'nervousness': admin.VERTICAL,
                    'nervous_moments': admin.VERTICAL,
                    'nightmares': admin.VERTICAL,
                    'disliked_by_othrs': admin.VERTICAL,
                    'constipated': admin.VERTICAL,
                    'anxiousness': admin.VERTICAL,
                    'feels_dizzy': admin.VERTICAL,
                    'feels_guity': admin.VERTICAL,
                    'overeating': admin.VERTICAL,
                    'overtired_noreason': admin.VERTICAL,
                    'overweight': admin.VERTICAL, }

    def export_as_csv(self, request, queryset):
        if request and request.POST.get('action', None) == 'export_as_csv':
            return super().export_as_csv(request, queryset)

    export_as_csv.short_description = _(
        'Export selected %(verbose_name_plural)s')

    actions = [export_as_csv]


@admin.register(ChildCBCLSection3, site=flourish_child_admin)
class ChildCBCLSection3Admin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    form = ChildCBCLSection3Form

    fieldsets = (
        ('Physical Problems without known medical cause:', {
            'fields': [
                'child_visit',
                'report_datetime',
                'body_aches',
                'headaches',
                'nauseous',
                'eye_prob',
                'eye_probl_desc',
                'skin_prob',
                'stomach_aches',
                'vomiting',
                'other_phys_prob',
                'attacks_physical',
                'body_picking',
                'picking_desc',
                'sexparts_public_play',
                'sexparts_play',
                'poor_schoolwork',
                'clumsy',
                'prefers_older_kids',
                'prefers_young_kids',
                'refuses_to_talk',
                'compulsions',
                'compulsions_desc',
                'home_runaway',
                'screams_alot',
                'secretive',
                'sight_hallucinations',
                'sh_desc',
                'self_conscious',
                'sets_fires',
                'sexual_prob',
                'sexual_prob_desc',
                'showing_off',
                'too_shy',
                'sleeps_less',
                'sleeps_more',
                'sleeps_more_desc',
                'inattentive',
                'speech_prob',
                'speech_prob_desc', ]},),
        audit_fieldset_tuple)

    radio_fields = {'body_aches': admin.VERTICAL,
                    'headaches': admin.VERTICAL,
                    'nauseous': admin.VERTICAL,
                    'eye_prob': admin.VERTICAL,
                    'skin_prob': admin.VERTICAL,
                    'stomach_aches': admin.VERTICAL,
                    'vomiting': admin.VERTICAL,
                    'attacks_physical': admin.VERTICAL,
                    'body_picking': admin.VERTICAL,
                    'sexparts_public_play': admin.VERTICAL,
                    'sexparts_play': admin.VERTICAL,
                    'poor_schoolwork': admin.VERTICAL,
                    'clumsy': admin.VERTICAL,
                    'prefers_older_kids': admin.VERTICAL,
                    'prefers_young_kids': admin.VERTICAL,
                    'refuses_to_talk': admin.VERTICAL,
                    'compulsions': admin.VERTICAL,
                    'home_runaway': admin.VERTICAL,
                    'screams_alot': admin.VERTICAL,
                    'secretive': admin.VERTICAL,
                    'sight_hallucinations': admin.VERTICAL,
                    'self_conscious': admin.VERTICAL,
                    'sets_fires': admin.VERTICAL,
                    'sexual_prob': admin.VERTICAL,
                    'showing_off': admin.VERTICAL,
                    'too_shy': admin.VERTICAL,
                    'sleeps_less': admin.VERTICAL,
                    'sleeps_more': admin.VERTICAL,
                    'inattentive': admin.VERTICAL,
                    'speech_prob': admin.VERTICAL, }

    def export_as_csv(self, request, queryset):
        if request and request.POST.get('action', None) == 'export_as_csv':
            return super().export_as_csv(request, queryset)

    export_as_csv.short_description = _(
        'Export selected %(verbose_name_plural)s')

    actions = [export_as_csv]


@admin.register(ChildCBCLSection4, site=flourish_child_admin)
class ChildCBCLSection4Admin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    form = ChildCBCLSection4Form
    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'stares_blankly',
                'steals_at_home',
                'steals_elsewhere',
                'hoarding',
                'hoarding_desc',
                'strange_behavior',
                'behavior_desc',
                'strange_ideas',
                'ideas_desc',
                'irritable',
                'sudden_mood_chng',
                'sulks_alot',
                'suspicious',
                'swearing',
                'self_harm_talks',
                'sleepwalk_talk',
                'sleepwalk_desc',
                'talks_alot',
                'teases_alot',
                'hot_temper',
                'sex_thoughts',
                'threatens_people',
                'thumbsucking',
                'smokes',
                'trouble_sleeping',
                'sleeping_desc',
                'skips_school',
                'underactive',
                'unhappy',
                'unusually_loud',
                'drug_usage',
                'drug_usage_desc',
                'vandalism',
                'daytime_wetting',
                'bedtime_wetting',
                'whining',
                'gender_dissonant',
                'withdrawn',
                'worries',
                'other_problems',
                'caregiver_interest',
                'caregiver_understanding',
                'valid',
                'invalid_reason',
                'other_invalid_reason',
                'impact_on_responses',
                'other_impact_on_responses',
                'overall_comments', ]},),
        audit_fieldset_tuple)

    radio_fields = {'stares_blankly': admin.VERTICAL,
                    'steals_at_home': admin.VERTICAL,
                    'steals_elsewhere': admin.VERTICAL,
                    'hoarding': admin.VERTICAL,
                    'strange_behavior': admin.VERTICAL,
                    'strange_ideas': admin.VERTICAL,
                    'irritable': admin.VERTICAL,
                    'sudden_mood_chng': admin.VERTICAL,
                    'sulks_alot': admin.VERTICAL,
                    'suspicious': admin.VERTICAL,
                    'swearing': admin.VERTICAL,
                    'self_harm_talks': admin.VERTICAL,
                    'sleepwalk_talk': admin.VERTICAL,
                    'talks_alot': admin.VERTICAL,
                    'teases_alot': admin.VERTICAL,
                    'hot_temper': admin.VERTICAL,
                    'sex_thoughts': admin.VERTICAL,
                    'threatens_people': admin.VERTICAL,
                    'thumbsucking': admin.VERTICAL,
                    'smokes': admin.VERTICAL,
                    'trouble_sleeping': admin.VERTICAL,
                    'skips_school': admin.VERTICAL,
                    'underactive': admin.VERTICAL,
                    'unhappy': admin.VERTICAL,
                    'unusually_loud': admin.VERTICAL,
                    'drug_usage': admin.VERTICAL,
                    'vandalism': admin.VERTICAL,
                    'daytime_wetting': admin.VERTICAL,
                    'bedtime_wetting': admin.VERTICAL,
                    'whining': admin.VERTICAL,
                    'gender_dissonant': admin.VERTICAL,
                    'withdrawn': admin.VERTICAL,
                    'worries': admin.VERTICAL,
                    'caregiver_interest': admin.VERTICAL,
                    'caregiver_understanding': admin.VERTICAL,
                    'valid': admin.VERTICAL,
                    'impact_on_responses': admin.VERTICAL,
                    'invalid_reason': admin.VERTICAL, }

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['fields_to_check'] = json.dumps([
            'caregiver_interest',
            'caregiver_understanding',
            'valid',
            'invalid_reason',
            'impact_on_responses',
        ])
        return super().changeform_view(request, object_id, form_url, extra_context)

    def export_as_csv(self, request, queryset):
        if request and request.POST.get('action', None) == 'export_as_csv':
            return super().export_as_csv(request, queryset)

    export_as_csv.short_description = _(
        'Export selected %(verbose_name_plural)s')

    actions = [export_as_csv]
