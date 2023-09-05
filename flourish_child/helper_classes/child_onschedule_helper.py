from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from edc_base.utils import get_utcnow, age
from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from .child_fu_booking_helper import ChildFollowUpBookingHelper


class ChildOnScheduleHelper(object):
    """A helper class that puts a child/infant into a particular schedule
    """

    child_offschedule_model = 'flourish_child.childoffschedule'

    def __init__(self, subject_identifier=None, base_appt_datetime=None, cohort=None, ):

        self.subject_identifier = subject_identifier
        self.base_appt_datetime = base_appt_datetime
        self.cohort = cohort

    @property
    def child_offschedule_cls(self):
        return django_apps.get_model(self.child_offschedule_model)

    def put_cohort_onschedule(self, instance, ):
        if self.cohort:
            instance.registration_update_or_create()
            if 'sec' in self.cohort or 'pool' in self.cohort:
                self.put_on_schedule(
                    instance,
                    cohort=self.cohort, )
            else:
                self.put_on_schedule(
                    instance,
                    cohort=(self.cohort + '_enrol'), )

    def put_on_schedule(self, instance, cohort=None, ):
        cohort = cohort or self.cohort
        if instance:
            subject_identifier = self.subject_identifier or instance.subject_identifier
    
            cohort_label_lower = ''.join(cohort.split('_'))
    
            if 'fuqt' in cohort_label_lower:
                cohort_label_lower = cohort_label_lower.replace('fuqt', 'fuquart')
    
            if 'enrol' in cohort:
                cohort_label_lower = cohort_label_lower.replace(
                    'enrol', 'enrollment')
    
            elif 'sec' in cohort:
                cohort_label_lower = cohort_label_lower.replace('qt', 'quart')
    
            if 'birth' in cohort:
                onschedule_model = 'flourish_child.onschedule' + cohort_label_lower
                schedule_name = cohort.replace('cohort_', '') + '_schedule1'
            else:
                onschedule_model = 'flourish_child.onschedulechild' + cohort_label_lower
    
                schedule_name = cohort.replace('cohort', 'child') + '_schedule1'
    
            if 'quarterly' in cohort:
                schedule_name = schedule_name.replace('quarterly', 'quart')
    
            if 'tb_adol' in cohort:
                schedule_name = 'tb_adol_schedule'
                onschedule_model = 'flourish_child.onschedulechildtbadolschedule'
    
            _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
                onschedule_model=onschedule_model, name=schedule_name)

            if not schedule.is_onschedule(subject_identifier=subject_identifier,
                                          report_datetime=self.base_appt_datetime):    
                schedule.put_on_schedule(
                    subject_identifier=subject_identifier,
                    onschedule_datetime=self.base_appt_datetime,
                    schedule_name=schedule_name,
                    base_appt_datetime=self.base_appt_datetime)
    
            if 'enrol' in cohort and 'sec' not in cohort:
                # book participant for followup
                booking_helper = ChildFollowUpBookingHelper()
                if not self.aging_out(subject_identifier):
                    booking_dt = self.base_appt_datetime + relativedelta(years=1)
                    booking_helper.schedule_fu_booking(subject_identifier, booking_dt)


    def get_onschedule_model_obj(self, schedule, query_key='subject_identifier',
                                 query_value=None):
        onschedule_model_cls = schedule.onschedule_model_cls
        try:
            return onschedule_model_cls.objects.get(
                **{f'{query_key}': query_value},)
        except onschedule_model_cls.DoesNotExist:
            return None

    def put_child_offschedule(self, schedule_name):
        if not (self.subject_identifier or schedule_name):
            raise Exception("Subject identifier or schedule name cannot be empty")
    
        try:
            offschedule_obj = self.child_offschedule_cls.objects.get(
                subject_identifier=self.subject_identifier,
                schedule_name=schedule_name)
        except self.child_offschedule_cls.DoesNotExist:
            self.child_offschedule_cls.objects.create(
                subject_identifier=self.subject_identifier,
                schedule_name=schedule_name,
                offschedule_datetime=get_utcnow())
        else:
            offschedule_obj.save()

    def aging_out(self, subject_identifier):
        """ Check if child is aging out before the year mark for follow-up
            booking arrives.
        """
        child_consent_cls = django_apps.get_model(
            'flourish_caregiver.caregiverchildconsent')
        try:
            latest_consent = child_consent_cls.objects.filter(
                subject_identifier=subject_identifier).latest('consent_datetime')
        except child_consent_cls.DoesNotExist:
            return False
        else:
            child_dob = latest_consent.child_dob
            if child_dob:
                child_age = age(child_dob, get_utcnow().date())
                age_in_years = (child_age.years + child_age.months/12)
                if age_in_years < 5 and round(5 - age_in_years, 2) < 1:
                    return round(5 - age_in_years, 2)
                elif age_in_years < 10 and round(10 - age_in_years, 2) < 1:
                    return round(10 - age_in_years, 2)
            return False
