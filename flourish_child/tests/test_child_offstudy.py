import datetime

from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from django.utils import timezone
from edc_base import get_utcnow
from edc_constants.constants import MALE, YES, INCOMPLETE
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy
from flourish_calendar.models import ParticipantNote
from flourish_caregiver.models import ScreeningPriorBhpParticipants

from ..helper_classes import ChildFollowUpBookingHelper
from ..helper_classes.child_fu_onschedule_helper import ChildFollowUpEnrolmentHelper
from ..models import OnScheduleChildCohortAEnrollment, OnScheduleChildCohortAFU, Appointment
from edc_visit_tracking.constants import SCHEDULED


@tag('offstudy-fu')
class TestChildOffstudy(TestCase):

    def setUp(self):
        import_holidays()
        self.booking_helper = ChildFollowUpBookingHelper
        self.fu_enrol_helper = ChildFollowUpEnrolmentHelper

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '1'
            }

        self.maternal_dataset_options = {
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-infected',
            'study_maternal_identifier': '12345',
            'protocol': 'Tshilo Dikotla'
            }

        self.child_dataset_options = {
            'infant_hiv_exposed': 'Exposed',
            'infant_enrolldate': get_utcnow(),
            'study_maternal_identifier': '12345',
            'study_child_identifier': '1234',
            'infant_sex': MALE
            }

        self.child_assent_options = {
            'gender': MALE,
            'first_name': 'TEST ONE',
            'last_name': 'TEST',
            'initials': 'TOT',
            'identity': '123425678',
            'identity_type': 'birth_cert',
            'confirm_identity': '123425678',
            'preg_testing': YES,
            'citizen': YES
            }

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            delivdt=get_utcnow() - relativedelta(years=3, months=0),
            **self.maternal_dataset_options)

        child_dataset = mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=3, months=0),
            **self.child_dataset_options)

        self.prior_screening = mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            study_maternal_identifier=maternal_dataset_obj.study_maternal_identifier
            )

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=YES,
            biological_caregiver=YES,
            **self.options)

        self.caregiver_child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            gender=MALE,
            study_child_identifier=child_dataset.study_child_identifier,
            child_dob=maternal_dataset_obj.delivdt.date(), )

        naive_datetime = datetime.datetime.combine(
            datetime.date(2025, 4, 30) - relativedelta(years=2), datetime.time())
        self.aware_datetime = timezone.make_aware(naive_datetime)

        mommy.make_recipe(
            'flourish_caregiver.caregiverpreviouslyenrolled',
            report_datetime=self.aware_datetime,
            subject_identifier=subject_consent.subject_identifier)

        onschedule_obj = OnScheduleChildCohortAEnrollment.objects.filter(
            subject_identifier=self.caregiver_child_consent.subject_identifier,
            schedule_name='child_a_enrol_schedule1')

        self.onschedule_dt = onschedule_obj[0].onschedule_datetime
        self.booking_dt = self.onschedule_dt + relativedelta(years=1)
        while self.booking_helper().check_date(self.booking_dt):
            self.booking_dt = self.booking_dt + relativedelta(days=1)

    def test_fu_booking_deleted(self):
        """ Assert followup booking is deleted on the calendar, if participant is
            taken offstudy before they are enroled in the followup schedule.
        """
        self.assertEqual(ParticipantNote.objects.filter(
            subject_identifier=self.caregiver_child_consent.subject_identifier,
            title='Follow Up Schedule',
            date=self.booking_dt.date()).count(), 1)

        mommy.make_recipe(
            'flourish_prn.childoffstudy',
            subject_identifier=self.caregiver_child_consent.subject_identifier,
            offstudy_date=self.onschedule_dt + relativedelta(months=5))

        self.assertEqual(ParticipantNote.objects.filter(
            subject_identifier=self.caregiver_child_consent.subject_identifier,
            title='Follow Up Schedule').count(), 0)

    def test_fu_booking_valid_if_enroled(self):
        """ Assert folloup booking is not removed if participant is taken offstudy
            already enroled on the followup schedule.
        """
        self.assertEqual(ParticipantNote.objects.filter(
            subject_identifier=self.caregiver_child_consent.subject_identifier,
            title='Follow Up Schedule',
            date=self.booking_dt.date()).count(), 1)
        appt = Appointment.objects.filter(
            subject_identifier=self.caregiver_child_consent.subject_identifier,
            schedule_name='child_a_enrol_schedule1')
        appt.update(appt_status=INCOMPLETE)
        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=appt[0],
            report_datetime=get_utcnow(),
            reason=SCHEDULED)
        subject_identifier = self.caregiver_child_consent.subject_identifier
        self.fu_enrol_helper(
            subject_identifier, update_mother=False).activate_child_fu_schedule()

        fu_onschedule = OnScheduleChildCohortAFU.objects.filter(
            subject_identifier=self.caregiver_child_consent.subject_identifier,)

        self.assertEqual(fu_onschedule.count(), 1)
        self.assertEqual(ParticipantNote.objects.filter(
            subject_identifier=self.caregiver_child_consent.subject_identifier,
            title='Follow Up Schedule',
            date=self.booking_dt.date()).count(), 1)
