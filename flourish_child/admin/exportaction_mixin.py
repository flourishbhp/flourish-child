from django.apps import apps as django_apps
from django.db.models import (FileField, ForeignKey, ImageField, ManyToManyField,
                              ManyToOneRel, OneToOneField)
from django.db.models.fields.reverse_related import OneToOneRel
from django.utils.translation import ugettext_lazy as _
from edc_base.utils import age
from edc_constants.constants import NEG, POS, YES

from flourish_export.admin_export_helper import AdminExportHelper


class ExportActionMixin(AdminExportHelper):
    tb_adol_assent_model = 'flourish_child.tbadolassent'

    @property
    def tb_adol_assent_cls(self):
        return django_apps.get_model(self.tb_adol_assent_model)

    def update_variables(self, data={}):
        """ Update study identifiers to desired variable name(s).
        """
        new_data_dict = {}
        replace_idx = {'subject_identifier': 'childpid',
                       'study_maternal_identifier': 'old_matpid',
                       'study_child_identifier': 'old_childpid'}
        for old_idx, new_idx in replace_idx.items():
            try:
                new_data_dict[new_idx] = data.pop(old_idx)
            except KeyError:
                continue
        new_data_dict.update(data)
        return new_data_dict

    def export_as_csv(self, request, queryset):
        records = []
        is_tb_adol_model = ('tb' in queryset[0].child_visit.schedule_name if hasattr(
            queryset[0], 'child_visit') else False) or (
                                   'TB Adol' in queryset[0].verbose_name)

        for obj in queryset:
            data = obj.__dict__.copy()

            subject_identifier = getattr(obj, 'subject_identifier', None)
            caregiver_sid = self.get_caregiver_sid(
                subject_identifier=subject_identifier)
            screening_identifier = self.screening_identifier(
                subject_identifier=caregiver_sid)
            previous_study = self.previous_bhp_study(
                subject_identifier=subject_identifier)
            study_maternal_identifier = self.study_maternal_identifier(
                screening_identifier=screening_identifier)
            child_exposure_status = self.child_hiv_exposure(
                subject_identifier=subject_identifier,
                study_maternal_identifier=study_maternal_identifier,
                caregiver_subject_identifier=caregiver_sid)
            visit_cohort = None

            # Add subject identifier and visit code
            if hasattr(obj, 'child_visit'):
                data_copy = data.copy()
                data.clear()
                visit_cohort = self.get_cohort_by_date(
                    subject_identifier, obj.child_visit.report_datetime)
                data.update(childpid=subject_identifier,
                            matpid=caregiver_sid,
                            old_matpid=study_maternal_identifier,
                            visit_code=obj.child_visit.visit_code,
                            **data_copy)

            # Update variable names for study identifiers
            data = self.update_variables(data)

            data.update(previous_study=previous_study,
                        child_exposure_status=child_exposure_status, )
            tb_age = self.tb_age_at_enrollment(subject_identifier)
            if is_tb_adol_model:
                data.update(tb_enrollment=tb_age)

            if obj._meta.label_lower == 'flourish_child.birthdata':
                infant_sex = self.infant_gender(subject_identifier)

                if is_tb_adol_model:
                    data.update(infant_sex=infant_sex)
                else:
                    data.update(infant_sex=infant_sex)

            for field in self.get_model_fields:
                field_name = field.name
                if isinstance(field, (ForeignKey, OneToOneField, OneToOneRel,)):
                    continue
                if isinstance(field, (FileField, ImageField,)):
                    file_obj = getattr(obj, field_name, '')
                    data.update({f'{field_name}': getattr(file_obj, 'name', '')})
                    continue
                if isinstance(field, ManyToManyField):
                    data.update(self.m2m_data_dict(obj, field))
                    continue
                if isinstance(field, ManyToOneRel):
                    data.update(self.inline_data_dict(obj, field))
                    continue
            # Update current and enrollment cohort
            enrol_cohort, current_cohort = self.get_cohort_details(subject_identifier)
            data.update(enrol_cohort=enrol_cohort,
                        current_cohort=current_cohort)
            if visit_cohort:
                data.update(visit_cohort=visit_cohort)

            # Exclude identifying values
            data = self.remove_exclude_fields(data)
            # Correct date formats
            data = self.fix_date_formats(data)
            records.append(data)

        response = self.write_to_csv(records)
        return response

    export_as_csv.short_description = _(
        'Export selected %(verbose_name_plural)s')

    actions = [export_as_csv]

    def caregiver_subject_consents(self, subject_identifier):
        consent_cls = django_apps.get_model(
            'flourish_caregiver.subjectconsent')
        return consent_cls.objects.filter(
            subject_identifier__endswith=subject_identifier)

    def screening_identifier(self, subject_identifier=None):
        """Returns a screening identifier.
        """
        consent = self.caregiver_subject_consents(subject_identifier)
        if consent:
            return consent.last().screening_identifier
        return None

    def get_caregiver_sid(self, subject_identifier):
        sub_subject_identifier = subject_identifier[1:-3]
        consent = self.caregiver_subject_consents(sub_subject_identifier)
        if consent.exists():
            return consent.earliest('consent_datetime').subject_identifier
        else:
            return None

    def previous_bhp_study(self, subject_identifier=None):
        caregiver_child_consent_cls = django_apps.get_model(
            'flourish_caregiver.caregiverchildconsent')
        if subject_identifier:
            try:
                caregiver_child_consent_obj = caregiver_child_consent_cls.objects.filter(
                    subject_identifier=subject_identifier).latest('consent_datetime')
            except caregiver_child_consent_cls.DoesNotExist:
                return None
            else:
                return caregiver_child_consent_obj.get_protocol

    def study_maternal_identifier(self, screening_identifier=None):
        dataset_cls = django_apps.get_model(
            'flourish_caregiver.maternaldataset')
        if screening_identifier:
            try:
                dataset_obj = dataset_cls.objects.get(
                    screening_identifier=screening_identifier)
            except dataset_cls.DoesNotExist:
                return None
            else:
                return dataset_obj.study_maternal_identifier

    def child_hiv_exposure(self, subject_identifier=None,
                           study_maternal_identifier=None,
                           caregiver_subject_identifier=None):

        child_dataset_cls = django_apps.get_model(
            'flourish_child.childdataset')

        if study_maternal_identifier:
            child_dataset_objs = child_dataset_cls.objects.filter(
                study_maternal_identifier=study_maternal_identifier)

            if child_dataset_objs:
                if child_dataset_objs[0].infant_hiv_exposed in ['Exposed', 'exposed']:
                    return 'HEU'
                elif child_dataset_objs[0].infant_hiv_exposed in ['Unexposed',
                                                                  'unexposed']:
                    return 'HUU'
        else:
            rapid_test_cls = django_apps.get_model(
                'flourish_caregiver.hivrapidtestcounseling')
            maternal_hiv_status = None

            try:
                rapid_test_obj = rapid_test_cls.objects.get(
                    maternal_visit__visit_code='1000M',
                    maternal_visit__visit_code_sequence=0,
                    maternal_visit__subject_identifier=caregiver_subject_identifier,
                    rapid_test_done=YES)
            except rapid_test_cls.DoesNotExist:
                antenatal_enrollment_cls = django_apps.get_model(
                    'flourish_caregiver.antenatalenrollment')
                try:
                    antenatal_enrollment = antenatal_enrollment_cls.objects.get(
                        subject_identifier=caregiver_subject_identifier,
                        child_subject_identifier=subject_identifier)
                except antenatal_enrollment_cls.DoesNotExist:
                    # To refactor to include new enrollees
                    maternal_hiv_status = 'UNK'
                else:
                    maternal_hiv_status = antenatal_enrollment.enrollment_hiv_status
            else:
                maternal_hiv_status = rapid_test_obj.result

            if maternal_hiv_status == POS:
                return 'HEU'
            elif maternal_hiv_status == NEG:
                return 'HUU'
            else:
                return 'UNK'

    def infant_gender(self, subject_identifier=None):

        child_consent_cls = django_apps.get_model(
            'flourish_caregiver.caregiverchildconsent')

        try:
            child_consent_obj = child_consent_cls.objects.filter(
                subject_identifier=subject_identifier, ).latest('consent_datetime')
        except child_consent_cls.DoesNotExist:
            pass
        else:
            return child_consent_obj.gender

    def tb_age_at_enrollment(self, subject_identifier=None):

        tb_adol_assent_cls = django_apps.get_model(
            'flourish_child.tbadolassent')

        try:
            tb_assent_obj = tb_adol_assent_cls.objects.get(
                subject_identifier=subject_identifier, )

        except tb_adol_assent_cls.DoesNotExist:
            pass
        else:
            return age(tb_assent_obj.dob,
                       tb_assent_obj.consent_datetime).years

    def is_non_crf(self, obj):
        if getattr(obj, 'subject_identifier'):
            return True
        else:
            return False

    @property
    def exclude_fields(self):
        return ['_state', 'hostname_created', 'hostname_modified',
                'revision', 'device_created', 'device_modified', 'id', 'site_id',
                'modified_time', 'report_datetime_time', 'registration_datetime_time',
                'screening_datetime_time', 'modified', 'form_as_json', 'consent_model',
                'randomization_datetime', 'registration_datetime', 'is_verified_datetime',
                'first_name', 'last_name', 'initials', 'guardian_name', 'identity',
                'infant_visit_id', 'maternal_visit_id', 'processed', 'processed_datetime',
                'packed', 'packed_datetime', 'shipped', 'shipped_datetime',
                'received_datetime', 'identifier_prefix', 'primary_aliquot_identifier',
                'clinic_verified', 'clinic_verified_datetime', 'drawn_datetime',
                'related_tracking_identifier', 'parent_tracking_identifier',
                'interview_file', 'interview_transcription', 'slug',
                'confirm_identity', 'site', 'subject_consent_id', '_django_version',
                'child_visit_id']

    @property
    def cohort_model_cls(self):
        return django_apps.get_model('flourish_caregiver.cohort')

    def get_cohort_details(self, subject_identifier):
        enrol_cohort = self.cohort_model_cls.objects.filter(
            subject_identifier=subject_identifier,
            enrollment_cohort=True).order_by('-assign_datetime').first()

        current_cohort = self.cohort_model_cls.objects.filter(
            subject_identifier=subject_identifier,
            current_cohort=True).order_by('-assign_datetime').first()

        enrol_name = getattr(enrol_cohort, 'name', None)
        current_name = getattr(current_cohort, 'name', None)

        return enrol_name, current_name

    def get_cohort_by_date(self, subject_identifier, report_datetime):
        """ Query cohort instances to get cohort details for a particular date.
            i.e. cohort participant was enrolled on at a specificied date.
            @param subject_identifier: child subject_identifier
            @param report_datetime: datetime to query for
            @return: cohort name
        """
        try:
            child_cohort = self.cohort_model_cls.objects.filter(
                subject_identifier=subject_identifier,
                assign_datetime__date__lte=report_datetime.date()).latest(
                'assign_datetime')
        except self.cohort_model_cls.DoesNotExist:
            return ''
        else:
            return child_cohort.name
