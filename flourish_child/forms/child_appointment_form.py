from django import forms
from django.apps import apps as django_apps
from edc_appointment.constants import NEW_APPT, IN_PROGRESS_APPT
from edc_appointment.form_validators import AppointmentFormValidator
from edc_base.sites.forms import SiteModelFormMixin
from edc_constants.constants import OPEN
from edc_form_validators import FormValidatorMixin
import pytz

from ..models import Appointment
from ..helper_classes.utils import child_utils


class AppointmentForm(SiteModelFormMixin, FormValidatorMixin, AppointmentFormValidator,
                      forms.ModelForm):
    """Note, the appointment is only changed, never added,
    through this form.
    """

    appointment_model = 'flourish_child.appointment'

    @property
    def data_action_item_cls(self):
        return django_apps.get_model('edc_data_manager.dataactionitem')

    def clean(self):
        super().clean()

        cleaned_data = self.cleaned_data

        if cleaned_data.get('appt_datetime'):

            visit_definition = self.instance.visits.get(self.instance.visit_code)

            earlist_appt_date = (self.instance.timepoint_datetime -
                                 visit_definition.rlower).astimezone(
                pytz.timezone('Africa/Gaborone'))
            latest_appt_date = (self.instance.timepoint_datetime +
                                visit_definition.rupper).astimezone(
                pytz.timezone('Africa/Gaborone'))

            if self.instance.visit_code_sequence == 0:
                if (cleaned_data.get('appt_datetime') < earlist_appt_date.replace(
                    microsecond=0)
                    or (self.instance.visit_code not in ['2000', '3000A', '3000B', '3000C']
                        and cleaned_data.get('appt_datetime') > latest_appt_date.replace(
                            microsecond=0))):
                    raise forms.ValidationError(
                        'The appointment datetime cannot be outside the window period, '
                        'please correct. See earliest, ideal and latest datetimes below.')
        self.validate_complete_cbcl_crfs()

    def validate_appt_new_or_complete(self):
        """
        Validates the caregiver appointment model by overriding existing appointment
        validation functions.
        """
        pass

    def validate_sequence(self):
        """Enforce appointment and visit entry sequence.
        """
        if self.cleaned_data.get('appt_status') == IN_PROGRESS_APPT:
            # visit report sequence
            prev_appt = None
            try:
                prev_appt = child_utils.get_previous_appt_instance(self.instance)
            except Appointment.DoesNotExist:
                pass
            
            if not getattr(prev_appt, 'childvisit', None):
                last_visit = self.appointment_model_cls.visit_model_cls().objects.filter(
                    appointment__subject_identifier=self.instance.subject_identifier,
                    visit_schedule_name=self.instance.visit_schedule_name,
                    report_datetime__lt=self.instance.appt_datetime
                ).order_by('appointment__appt_datetime').last()

                if last_visit:
                    try:
                        next_visit = last_visit.appointment.get_next_by_appt_datetime(
                            subject_identifier=self.instance.subject_identifier,
                            visit_schedule_name=self.instance.visit_schedule_name)
                    except last_visit.appointment.DoesNotExist:
                        raise forms.ValidationError(
                            f'A previous visit report is required. Enter the visit report for '
                            f'appointment {next_visit.visit_code} before '
                            'starting with this appointment.')
 
            # appointment sequence
            try:
                prev_appt = child_utils.get_previous_appt_instance(self.instance)
            except Appointment.DoesNotExist:
                pass
            if not getattr(prev_appt, 'childvisit', None):
                first_new_appt = self.appointment_model_cls.objects.filter(
                    subject_identifier=self.instance.subject_identifier,
                    visit_schedule_name=self.instance.visit_schedule_name,
                    appt_status=NEW_APPT,
                    appt_datetime__lt=self.instance.appt_datetime
                ).order_by('appt_datetime').first()
                if first_new_appt:
                    raise forms.ValidationError(
                        'A previous appointment requires updating. '
                        f'Update appointment for {first_new_appt.visit_code} first.')

    def validate_complete_cbcl_crfs(self):
        appointment = self.instance
        cbcl_crfs = ['childcbclsection1', 'childcbclsection2',
                     'childcbclsection3', 'childcbclsection4']

        cbcl_objs = []

        for cbcl_form in cbcl_crfs:
            model_cls = django_apps.get_model(f'flourish_child.{cbcl_form}')
            try:
                model_obj = model_cls.objects.get(child_visit__appointment=appointment)
            except model_cls.DoesNotExist:
                continue
            else:
                cbcl_objs.append(model_obj)

        if cbcl_objs and len(cbcl_objs) < 4:
            subject_identifier = appointment.subject_identifier
            visit_code = appointment.visit_code
            self.create_data_action_item(
                visit_code=visit_code, subject_identifier=subject_identifier)

    def create_data_action_item(self, visit_code=None, subject_identifier=None):

        defaults = {
            'assigned': 'clinic',
            'comment': (f'The CBCL CRFs are not all completed at visit {visit_code} for '
                        f'participant {subject_identifier}, Please complete all the forms.'),
            'action_priority': 'high',
            'status': OPEN
        }

        self.data_action_item_cls.objects.update_or_create(
            subject_identifier=subject_identifier,
            subject=(f'Please complete all the CBCL CRFs at visit {visit_code} for PID '
                     f'{subject_identifier}.'),
            defaults=defaults, )

    class Meta:
        model = Appointment
        fields = '__all__'
