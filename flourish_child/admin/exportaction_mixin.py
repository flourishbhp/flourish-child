import datetime
import uuid

from django.apps import apps as django_apps
from django.db.models import ManyToManyField, ForeignKey, OneToOneField, ManyToOneRel
from django.http import HttpResponse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import xlwt


class ExportActionMixin:

    def export_as_csv(self, request, queryset):

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s.xls' % (
            self.get_export_filename())

        wb = xlwt.Workbook(encoding='utf-8', style_compression=2)
        ws = wb.add_sheet('%s')

        row_num = 0
        obj_count = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        font_style.num_format_str = 'YYYY/MM/DD h:mm:ss'

        field_names = [field.name for field in self.get_model_fields]

        if queryset and self.is_assent(queryset[0]):
            field_names.insert(0, 'previous_study')

        if queryset and getattr(queryset[0], 'child_visit', None):
            field_names.insert(0, 'subject_identifier')
            field_names.insert(1, 'new_maternal_study_subject_identifier')
            field_names.insert(2, 'old_study_maternal_identifier')
            field_names.insert(3, 'previous_study')
            field_names.insert(4, 'visit_code')

        for col_num in range(len(field_names)):
            ws.write(row_num, col_num, field_names[col_num], font_style)

        for obj in queryset:
            data = []

            # Add subject identifier and visit code
            if getattr(obj, 'child_visit', None):
                obj_data['visit_code'] = obj.child_visit.visit_code
                obj_data['subject_identifier'] = obj.child_visit.subject_identifier

            subject_identifier = obj_data.get('subject_identifier', None)
            screening_identifier = self.screening_identifier(subject_identifier=subject_identifier[:-3])
            previous_study = self.previous_bhp_study(screening_identifier=screening_identifier)
            study_maternal_identifier = self.study_maternal_identifier(screening_identifier=screening_identifier)
            obj_data['new_maternal_study_subject_identifier'] = subject_identifier[:-3]
            obj_data['previous_study'] = previous_study
            obj_data['old_study_maternal_identifier'] = study_maternal_identifier
            obj_data['on_study'] = self.on_study(subject_identifier=subject_identifier)

            data = [obj_data[field] for field in field_names]

            row_num += 1
            for col_num in range(len(data)):
                if isinstance(data[col_num], uuid.UUID):
                    ws.write(row_num, col_num, str(data[col_num]))
                elif isinstance(data[col_num], datetime.datetime):
                    data[col_num] = timezone.make_naive(data[col_num])
                    ws.write(row_num, col_num, data[col_num], xlwt.easyxf(num_format_str='YYYY/MM/DD h:mm:ss'))
                else:
                    ws.write(row_num, col_num, data[col_num])
            #     subject_identifier = obj.child_visit.subject_identifier
            #     screening_identifier = self.screening_identifier(subject_identifier=subject_identifier[:-3])
            #     previous_study = self.previous_bhp_study(screening_identifier=screening_identifier)
            #     study_maternal_identifier = self.study_maternal_identifier(screening_identifier=screening_identifier)
            #     data.append(subject_identifier)
            #     data.append(subject_identifier[:-3])
            #     data.append(study_maternal_identifier)
            #     data.append(previous_study)
            #     data.append(obj.child_visit.visit_code)
            # elif self.is_assent(obj):
            #     subject_identifier = getattr(obj, 'subject_identifier')
            #     screening_identifier = self.screening_identifier(subject_identifier=subject_identifier[:-3])
            #     previous_study = self.previous_bhp_study(screening_identifier=screening_identifier)
            #     data.append(previous_study)

            inline_objs = []
            for field in self.get_model_fields:
                if isinstance(field, ManyToManyField):
                    key_manager = getattr(obj, field.name)
                    field_value = ', '.join([obj.name for obj in key_manager.all()])
                    data.append(field_value)
                    continue
                if isinstance(field, (ForeignKey, OneToOneField, )):
                    field_value = getattr(obj, field.name)
                    data.append(field_value.id)
                    continue
                if isinstance(field, ManyToOneRel):
                    key_manager = getattr(obj, f'{field.name}_set')
                    inline_objs = key_manager.all()
                field_value = getattr(obj, field.name, '')
                data.append(field_value)

            if inline_objs:
                # Update header
                inline_fields = inline_objs[0].__dict__
                inline_fields = self.inline_exclude(field_names=inline_fields)
                inline_fields = list(inline_fields.keys())
                if obj_count == 0:
                    self.update_headers_inline(
                        inline_fields=inline_fields, field_names=field_names,
                        ws=ws, row_num=row_num, font_style=font_style)

                for inline_obj in inline_objs:
                    inline_data = []
                    inline_data.extend(data)
                    for field in inline_fields:
                        field_value = getattr(inline_obj, field, '')
                        inline_data.append(field_value)
                    row_num += 1
                    self.write_rows(data=inline_data, row_num=row_num, ws=ws)
            else:
                row_num += 1
                self.write_rows(data=data, row_num=row_num, ws=ws)
            obj_count += 1
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
                ws.write(row_num, col_num, dt, xlwt.easyxf(num_format_str='YYYY/MM/DD h:mm:ss'))
            elif isinstance(data[col_num], datetime.date):
                ws.write(row_num, col_num, data[col_num], xlwt.easyxf(num_format_str='YYYY/MM/DD'))
            else:
                ws.write(row_num, col_num, data[col_num])

    def update_headers_inline(self, inline_fields=None, field_names=None,
                              ws=None, row_num=None, font_style=None):
        top_num = len(field_names)
        for col_num in range(len(inline_fields)):
            ws.write(row_num, top_num, inline_fields[col_num], font_style)
            top_num += 1

    def get_export_filename(self):
        date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        filename = "%s-%s" % (self.model.__name__, date_str)
        return filename

    def screening_identifier(self, subject_identifier=None):
        """Returns a screening identifier.
        """
        consent_cls = django_apps.get_model('flourish_caregiver.subjectconsent')
        consent = consent_cls.objects.filter(subject_identifier=subject_identifier)
        if consent:
            return consent.last().screening_identifier
        return None

    def previous_bhp_study(self, screening_identifier=None):
        dataset_cls = django_apps.get_model('flourish_caregiver.maternaldataset')
        if screening_identifier:
            try:
                dataset_obj = dataset_cls.objects.get(
                    screening_identifier=screening_identifier)
            except dataset_cls.DoesNotExist:
                return None
            else:
                return dataset_obj.protocol

    def study_maternal_identifier(self, screening_identifier=None):
        dataset_cls = django_apps.get_model('flourish_caregiver.maternaldataset')
        if screening_identifier:
            try:
                dataset_obj = dataset_cls.objects.get(
                    screening_identifier=screening_identifier)
            except dataset_cls.DoesNotExist:
                return None
            else:
                return dataset_obj.study_maternal_identifier

    def is_assent(self, obj):
        assent_cls = django_apps.get_model('flourish_child.childassent')
        return isinstance(obj, assent_cls)

    @property
    def get_model_fields(self):
        return self.model._meta.get_fields()

    def inline_exclude(self, field_names={}):
        exclude = ['_state', 'revision', 'hostname_modified', 'hostname_created',
                   'user_modified', 'user_created', 'device_created', 'device_modified']
        for field in exclude:
            del field_names[field]
        return field_names
