import datetime
import uuid
import xlwt

from django.apps import apps as django_apps
from django.db.models import (ManyToManyField, ForeignKey, OneToOneField, ManyToOneRel,
                              FileField, ImageField)
from django.db.models.fields.reverse_related import OneToOneRel
from django.http import HttpResponse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from edc_constants.constants import NEG, POS, YES
from edc_base.utils import age

from ..helper_classes.utils import child_utils


class ExportActionMixin:

    tb_adol_assent_model = 'flourish_child.tbadolassent'

    @property
    def tb_adol_assent_cls(self):
        return django_apps.get_model(self.tb_adol_assent_model)

    def export_as_csv(self, request, queryset):

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s.xls' % (
            self.get_export_filename())

        wb = xlwt.Workbook(encoding='utf-8', style_compression=2)
        ws = wb.add_sheet('%s')

        row_num = 0
        obj_count = 0
        self.inline_header = False

        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        font_style.num_format_str = 'YYYY/MM/DD h:mm:ss'

        field_names = []
        for field in self.get_model_fields:
            if isinstance(field, ManyToManyField):
                choices = self.m2m_list_data(field.related_model)
                for choice in choices:
                    field_names.append(choice)
                continue
            field_names.append(field.name)
        field_names.extend(['enrollment_cohort', 'current_cohort', ])
        is_tb_adol_model = ('tb' in queryset[0].child_visit.schedule_name if hasattr(
            queryset[0], 'child_visit') else False) or ('TB Adol' in queryset[0].verbose_name)

        if queryset and self.is_non_crf(queryset[0]):
            field_names.insert(0, 'previous_study')
            field_names.insert(1, 'child_exposure_status')
            if is_tb_adol_model:
                field_names.insert(2, 'tb_enrollment')

        if queryset and getattr(queryset[0], 'child_visit', None):
            field_names.insert(0, 'subject_identifier')
            field_names.insert(1, 'new_maternal_study_subject_identifier')
            field_names.insert(2, 'old_study_maternal_identifier')

            if is_tb_adol_model:
                field_names.insert(6, 'visit_code')
            else:
                field_names.insert(5, 'visit_code')

        if queryset[0]._meta.label_lower == 'flourish_child.birthdata':
            if is_tb_adol_model:
                field_names.insert(5, 'infant_sex')
            else:
                field_names.insert(4, 'infant_sex')

        for col_num in range(len(field_names)):
            ws.write(row_num, col_num, field_names[col_num], font_style)

        for obj in queryset:
            data = []
            inline_field_names = []

            # Add subject identifier and visit code
            if hasattr(obj, 'child_visit'):
                subject_identifier = obj.child_visit.subject_identifier
                caregiver_sid = child_utils.caregiver_subject_identifier(
                    subject_identifier=subject_identifier)

                screening_identifier = self.screening_identifier(
                    subject_identifier=caregiver_sid)
                previous_study = self.previous_bhp_study(
                    subject_identifier=subject_identifier)
                study_maternal_identifier = self.study_maternal_identifier(
                    screening_identifier=screening_identifier)
                child_exposure_status = self.child_hiv_exposure(
                    study_maternal_identifier, caregiver_sid)

                tb_age = self.tb_age_at_enrollment(subject_identifier)

                data.append(subject_identifier)
                data.append(caregiver_sid)
                data.append(study_maternal_identifier)
                data.append(previous_study)
                data.append(child_exposure_status)
                if is_tb_adol_model:
                    data.append(tb_age)
                data.append(obj.child_visit.visit_code)

            elif self.is_non_crf(obj):
                subject_identifier = getattr(obj, 'subject_identifier', None)
                caregiver_sid = child_utils.caregiver_subject_identifier(
                    subject_identifier=subject_identifier)

                screening_identifier = self.screening_identifier(
                    subject_identifier=caregiver_sid)
                previous_study = self.previous_bhp_study(
                    subject_identifier=subject_identifier)
                study_maternal_identifier = self.study_maternal_identifier(
                    screening_identifier=screening_identifier)
                child_exposure_status = self.child_hiv_exposure(
                    subject_identifier, study_maternal_identifier, caregiver_sid)

                tb_age = self.tb_age_at_enrollment(subject_identifier)

                data.append(previous_study)
                data.append(child_exposure_status)
                if is_tb_adol_model:
                    data.append(tb_age)

            if obj._meta.label_lower == 'flourish_child.birthdata':
                infant_sex = self.infant_gender(subject_identifier)

                if is_tb_adol_model:
                    data.append(infant_sex)
                else:
                    data.insert(4, infant_sex)

            inline_objs = []
            for field in self.get_model_fields:

                if isinstance(field, (FileField, ImageField,)):
                    file_obj = getattr(obj, field.name, '')
                    data.append(getattr(file_obj, 'name', ''))
                    continue
                if isinstance(field, ManyToManyField):
                    m2m_values = self.get_m2m_values(obj, m2m_field=field)
                    data.extend(m2m_values)
                    continue
                if isinstance(field, (ForeignKey, OneToOneField)):
                    field_value = getattr(obj, field.name)
                    data.append(field_value.id)
                    continue
                if isinstance(field, OneToOneRel):
                    continue
                if isinstance(field, ManyToOneRel):
                    key_manager = getattr(obj, f'{field.name}_set',
                                          getattr(obj, f'{field.related_name}', None))
                    inline_values = key_manager.all()
                    fields = field.related_model._meta.get_fields()
                    for field in fields:
                        if not isinstance(field, (ForeignKey, OneToOneField, ManyToManyField,)):
                            inline_field_names.append(field.name)
                        if isinstance(field, ManyToManyField):
                            choices = self.m2m_list_data(field.related_model)
                            inline_field_names.extend(
                                [choice for choice in choices])
                    if inline_values:
                        inline_objs.append(inline_values)
                field_value = getattr(obj, field.name, '')
                data.append(field_value)
            
            # Add current and enrollment cohort
            enrol_cohort, current_cohort = self.get_cohort_details(subject_identifier)
            data.extend([enrol_cohort, current_cohort])

            if inline_objs:
                # Update header
                inline_field_names = self.inline_exclude(
                    field_names=inline_field_names)
                if not self.inline_header:
                    self.update_headers_inline(
                        inline_fields=inline_field_names, field_names=field_names,
                        ws=ws, row_num=0, font_style=font_style)

                for inline_qs in inline_objs:
                    for inline_obj in inline_qs:
                        inline_data = []
                        inline_data.extend(data)
                        for field in inline_obj._meta.get_fields():
                            if isinstance(field, (FileField, ImageField,)):
                                file_obj = getattr(inline_obj, field.name, '')
                                inline_data.append(getattr(file_obj, 'name', ''))
                                continue
                            if field.name in inline_field_names:
                                inline_data.append(
                                    getattr(inline_obj, field.name, ''))
                            if isinstance(field, ManyToManyField):
                                m2m_values = self.get_m2m_values(
                                    inline_obj, m2m_field=field)
                                inline_data.extend(m2m_values)
                        row_num += 1
                        self.write_rows(data=inline_data,
                                        row_num=row_num, ws=ws)
                obj_count += 1
            else:
                row_num += 1
                self.write_rows(data=data, row_num=row_num, ws=ws)
        wb.save(response)
        return response

    export_as_csv.short_description = _(
        'Export selected %(verbose_name_plural)s')

    actions = [export_as_csv]

    def write_rows(self, data=None, row_num=None, ws=None):
        for col_num in range(len(data)):
            if isinstance(data[col_num], uuid.UUID):
                ws.write(row_num, col_num, str(data[col_num]))
            elif isinstance(data[col_num], datetime.datetime):
                dt = data[col_num]
                if dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None:
                    dt = timezone.make_naive(dt)
                dt = dt.strftime('%Y/%m/%d')
                ws.write(row_num, col_num, dt, xlwt.easyxf(
                    num_format_str='YYYY/MM/DD'))
            elif isinstance(data[col_num], datetime.date):
                ws.write(row_num, col_num, data[col_num], xlwt.easyxf(
                    num_format_str='YYYY/MM/DD'))
            else:
                ws.write(row_num, col_num, data[col_num])

    def update_headers_inline(self, inline_fields=None, field_names=None,
                              ws=None, row_num=None, font_style=None):
        top_num = len(field_names)
        for col_num in range(len(inline_fields)):
            ws.write(row_num, top_num, inline_fields[col_num], font_style)
            top_num += 1
            self.inline_header = True

    def get_export_filename(self):
        date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        filename = "%s-%s" % (self.model.__name__, date_str)
        return filename

    def screening_identifier(self, subject_identifier=None):
        """Returns a screening identifier.
        """
        consent_cls = django_apps.get_model(
            'flourish_caregiver.subjectconsent')
        consent = consent_cls.objects.filter(
            subject_identifier=subject_identifier)
        if consent:
            return consent.last().screening_identifier
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
                elif child_dataset_objs[0].infant_hiv_exposed in ['Unexposed', 'unexposed']:
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
                subject_identifier=subject_identifier,).latest('consent_datetime')
        except child_consent_cls.DoesNotExist:
            pass
        else:
            return child_consent_obj.gender

    def tb_age_at_enrollment(self, subject_identifier=None):

        tb_adol_assent_cls = django_apps.get_model(
            'flourish_child.tbadolassent')

        try:
            tb_assent_obj = tb_adol_assent_cls.objects.get(
                subject_identifier=subject_identifier,)

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
    def get_model_fields(self):
        return [field for field in self.model._meta.get_fields()
                if field.name not in self.exclude_fields and not isinstance(field, OneToOneRel)]

    @property
    def exclude_fields(self):
        return ['created', '_state', 'hostname_created', 'hostname_modified',
                'revision', 'device_created', 'device_modified', 'id', 'site_id',
                'created_time', 'modified_time', 'report_datetime_time',
                'registration_datetime_time', 'screening_datetime_time', 'modified',
                'form_as_json', 'consent_model', 'randomization_datetime',
                'registration_datetime', 'is_verified_datetime', 'first_name',
                'last_name', 'initials', 'guardian_name', 'identity', 'infant_visit_id',
                'maternal_visit_id', 'processed', 'processed_datetime', 'packed',
                'packed_datetime', 'shipped', 'shipped_datetime', 'received_datetime',
                'identifier_prefix', 'primary_aliquot_identifier', 'clinic_verified',
                'clinic_verified_datetime', 'drawn_datetime', 'related_tracking_identifier',
                'parent_tracking_identifier', 'interview_file', 'interview_transcription']

    def inline_exclude(self, field_names=[]):
        return [field_name for field_name in field_names
                if field_name not in self.exclude_fields]

    def m2m_list_data(self, model_cls=None):
        qs = model_cls.objects.order_by(
            'created').values_list('short_name', flat=True)
        return list(qs)

    def get_m2m_values(self, model_obj, m2m_field=None):
        m2m_values = []
        model_cls = m2m_field.related_model
        choices = self.m2m_list_data(model_cls=model_cls)
        key_manager = getattr(model_obj, m2m_field.name)
        for choice in choices:
            selected = 0
            try:
                key_manager.get(short_name=choice)
            except model_cls.DoesNotExist:
                pass
            else:
                selected = 1
            m2m_values.append(selected)
        return m2m_values

    def get_cohort_details(self, subject_identifier):
        cohort_model_cls = django_apps.get_model('flourish_caregiver.cohort')
        enrol_cohort = cohort_model_cls.objects.filter(
            subject_identifier=subject_identifier,
            enrollment_cohort=True).order_by('-assign_datetime').first()
        
        current_cohort = cohort_model_cls.objects.filter(
            subject_identifier=subject_identifier,
            current_cohort=True).order_by('-assign_datetime').first()

        enrol_name = getattr(enrol_cohort, 'name', None)
        current_name = getattr(current_cohort, 'name', None)

        return enrol_name, current_name
