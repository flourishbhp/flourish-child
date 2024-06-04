from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from flourish_caregiver.helper_classes.fu_onschedule_helper import FollowUpEnrolmentHelper

from django.db.models import Q
from edc_appointment.constants import NEW_APPT
from edc_base.utils import get_utcnow

from .utils import child_utils
from ..models import Appointment
from ..models import ChildOffSchedule
from ..models import OnScheduleChildCohortAFU, OnScheduleChildCohortBFU
from ..models import OnScheduleChildCohortBFUQuart, OnScheduleChildCohortCFUQuart
from ..models import OnScheduleChildCohortCFU, OnScheduleChildCohortAFUQuart


class ChildFollowUpEnrolmentHelper(object):
    """Class that puts participant into a followup schedule and reschedules
     consecutive follow ups.

    * Accepts an registered_subject of RegisteredSubject.
    * is called in the dashboard view for subject.

    """

    def __init__(self, subject_identifier, onschedule_datetime=None, update_mother=True):

        self.subject_identifier = subject_identifier
        self.onschedule_datetime = onschedule_datetime
        self.update_mother = update_mother

        self.cohort_dict = {'a': OnScheduleChildCohortAFU,
                            'b': OnScheduleChildCohortBFU,
                            'c': OnScheduleChildCohortCFU, }

        self.cohort_quart_dict = {'a': OnScheduleChildCohortAFUQuart,
                                  'b': OnScheduleChildCohortBFUQuart,
                                  'c': OnScheduleChildCohortCFUQuart, }

    def get_latest_completed_child_appointment(self, subject_identifier):
        """ Get latest child appointment that was started/completed given the
         subject identifier """

        appts = Appointment.objects.filter(
            ~Q(appt_status=NEW_APPT) & ~Q(schedule_name__icontains='sec'),
            subject_identifier=subject_identifier).exclude(
            schedule_name__icontains='tb')

        if appts:
            latest = appts.order_by('timepoint').last()
            return latest

    def child_off_current_schedule(self, latest_appointment):

        if latest_appointment:
            quart_appt = Appointment.objects.filter(
                subject_identifier=latest_appointment.subject_identifier,
                schedule_name__icontains='quart').latest('-appt_datetime')

            try:
                offschedule_obj = ChildOffSchedule.objects.get(
                    subject_identifier=quart_appt.subject_identifier,
                    schedule_name=quart_appt.schedule_name)
            except ChildOffSchedule.DoesNotExist:
                ChildOffSchedule.objects.create(
                    subject_identifier=quart_appt.subject_identifier,
                    schedule_name=quart_appt.schedule_name,
                    offschedule_datetime=get_utcnow())
            else:
                offschedule_obj.save()

            return quart_appt.schedule_name

    def put_on_child_fu_schedule(self, schedule_name, subject_identifier):
        """ Take child offschedule for quarterly schedule and put them on the follow up
         schedule and its consecutive quarterly calls. Children on Secondary Aims are not
         considered.
        """

        vs = schedule_name.split('_')

        if 'enrol' in schedule_name:
            schedule_name = '_'.join([vs[0], vs[1], vs[2].replace('enrol', 'fu'), vs[3]])
        elif 'qt' in schedule_name:
            schedule_name = '_'.join([vs[0], vs[1], vs[2].replace('sec', 'fu'), vs[3]])
        elif 'birth' in schedule_name:
            schedule_name = '_'.join([vs[0], vs[1], vs[2].replace('birth', 'fu'), vs[3]])
        else:
            schedule_name = '_'.join([vs[0], vs[1], vs[2].replace('quart', 'fu'), vs[3]])

        onschedule_model_cls = self.cohort_dict.get(vs[1])

        _, new_schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            name=schedule_name,
            onschedule_model=onschedule_model_cls._meta.label_lower)

        new_schedule.put_on_schedule(
            onschedule_datetime=self.onschedule_datetime,
            subject_identifier=subject_identifier,
            schedule_name=schedule_name)

    def activate_child_fu_schedule(self):

        latest_child_appt = self.get_latest_completed_child_appointment(
            self.subject_identifier)

        if latest_child_appt and 'sec' not in latest_child_appt.schedule_name:

            self.child_off_current_schedule(latest_child_appt)

            self.put_on_child_fu_schedule(latest_child_appt.schedule_name,
                                          latest_child_appt.subject_identifier)

            if self.update_mother:
                cohort = latest_child_appt.schedule_name.split('_')[1]
                schedule_number = latest_child_appt.schedule_name[-1]
                caregiver_pid = child_utils.caregiver_subject_identifier(
                    subject_identifier=self.subject_identifier)
                schedule_enrol_helper = FollowUpEnrolmentHelper(
                    subject_identifier=caregiver_pid,
                    cohort=cohort,
                    schedule_number=schedule_number)
                schedule_enrol_helper.activate_fu_schedule()
