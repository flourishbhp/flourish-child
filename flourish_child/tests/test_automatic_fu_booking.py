import datetime
from unittest.case import skip

from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.test import tag, TestCase
from django.utils import timezone
from edc_appointment.models import Appointment as CaregiverAppointment
from edc_base import get_utcnow
from edc_constants.constants import FEMALE, MALE, NEG, NOT_APPLICABLE, YES
from edc_facility.import_holidays import import_holidays
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy

from flourish_calendar.models import ParticipantNote
from ..helper_classes import ChildFollowUpBookingHelper
from ..models import (ChildDummySubjectConsent, OnScheduleChildCohortABirth,
                      OnScheduleChildCohortAEnrollment, OnScheduleChildCohortCSec)

app_config = django_apps.get_app_config('flourish_child')


@tag('booking')
class TestFuBooking(TestCase):

    def setUp(self):
        import_holidays()
        self.booking_helper = ChildFollowUpBookingHelper

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': app_config.consent_version
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

        mommy.make_recipe(
            'flourish_caregiver.flourishconsentversion',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            version=app_config.consent_version,
            child_version=app_config.consent_version)

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,
        )

        self.subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=YES,
            biological_caregiver=YES,
            **self.options)

        self.caregiver_child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=self.subject_consent,
            gender=MALE,
            study_child_identifier=child_dataset.study_child_identifier,
            child_dob=maternal_dataset_obj.delivdt.date(), )

        naive_datetime = datetime.datetime.combine(
            datetime.date(2025, 4, 30) - relativedelta(years=2), datetime.time())
        self.aware_datetime = timezone.make_aware(naive_datetime)

        mommy.make_recipe(
            'flourish_caregiver.caregiverpreviouslyenrolled',
            report_datetime=self.aware_datetime,
            subject_identifier=self.subject_consent.subject_identifier)

    @tag('fub')
    def test_fu_booking(self):
        self.assertEqual(ChildDummySubjectConsent.objects.filter(
            identity=self.caregiver_child_consent.identity).count(), 1)

        onschedule_obj = OnScheduleChildCohortAEnrollment.objects.filter(
            subject_identifier=self.caregiver_child_consent.subject_identifier,
            schedule_name='child_a_enrol_schedule1')
        self.assertEqual(onschedule_obj.count(), 1)

        onschedule_dt = onschedule_obj[0].onschedule_datetime
        booking_dt = onschedule_dt + relativedelta(years=1)
        while self.booking_helper().check_date(booking_dt):
            booking_dt = booking_dt + relativedelta(days=1)

        self.assertEqual(ParticipantNote.objects.filter(
            subject_identifier=self.caregiver_child_consent.subject_identifier,
            title='Follow Up Schedule',
            date=booking_dt.date()).count(), 1)

    def test_fu_booking_birth(self):
        screening_preg = mommy.make_recipe(
            'flourish_caregiver.screeningpregwomen',
        )

        preg_subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=screening_preg.screening_identifier,
            breastfeed_intent=YES,
            gender=FEMALE,
            **self.options)

        preg_caregiver_child_consent_obj = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=preg_subject_consent,
            gender=None,
            first_name=None,
            last_name=None,
            identity=None,
            confirm_identity=None,
            study_child_identifier=None,
            child_dob=None,
            version=app_config.consent_version)

        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            current_hiv_status=NEG,
            child_subject_identifier=preg_caregiver_child_consent_obj.subject_identifier,
            subject_identifier=preg_subject_consent.subject_identifier, )

        caregiver_visit = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=CaregiverAppointment.objects.get(
                subject_identifier=preg_subject_consent.subject_identifier,
                visit_code='1000M'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_caregiver.ultrasound',
            child_subject_identifier=preg_caregiver_child_consent_obj.subject_identifier,
            maternal_visit=caregiver_visit, )

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            subject_identifier=preg_subject_consent.subject_identifier,
            child_subject_identifier=preg_caregiver_child_consent_obj.subject_identifier,
            delivery_datetime=self.aware_datetime,
            live_infants_to_register=1)

        mommy.make_recipe(
            'flourish_child.childbirth',
            subject_identifier=preg_caregiver_child_consent_obj.subject_identifier,
            dob=self.aware_datetime.date(),
            gender=MALE)

        self.assertEqual(OnScheduleChildCohortABirth.objects.filter(
            subject_identifier=preg_caregiver_child_consent_obj.subject_identifier,
            schedule_name='child_a_birth_schedule1').count(), 1)

        self.assertEqual(ParticipantNote.objects.filter(
            subject_identifier=preg_caregiver_child_consent_obj.subject_identifier,
            title='Follow Up Schedule', ).count(), 1)

    @skip("Test performed with max part as 1, now changed to 3. Expected to fail.")
    def test_fu_booking_rescheduling(self):
        """ NB: Test was performed with max participant's to be booked in a day
            set as 1.
        """
        self.maternal_dataset_options.update(study_maternal_identifier='4321')
        self.child_dataset_options.update(study_maternal_identifier='4321',
                                          study_child_identifier='2314')

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            delivdt=get_utcnow() - relativedelta(years=3, months=6),
            **self.maternal_dataset_options)

        child_dataset_obj = mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=3, months=6),
            **self.child_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,
        )

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=YES,
            biological_caregiver=YES,
            **self.options)

        caregiver_child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            gender=MALE,
            study_child_identifier=child_dataset_obj.study_child_identifier,
            child_dob=maternal_dataset_obj.delivdt.date(), )

        mommy.make_recipe(
            'flourish_caregiver.caregiverpreviouslyenrolled',
            subject_identifier=subject_consent.subject_identifier)

        onschedule_obj = OnScheduleChildCohortAEnrollment.objects.filter(
            schedule_name='child_a_enrol_schedule1')
        self.assertEqual(onschedule_obj.count(), 2)

        booking_dt = onschedule_obj[0].onschedule_datetime + relativedelta(years=1)
        while self.booking_helper().check_date(booking_dt):
            booking_dt = booking_dt + relativedelta(days=1)
        rescheduled_dt = booking_dt + relativedelta(days=1)
        while self.booking_helper().check_date(rescheduled_dt):
            rescheduled_dt = rescheduled_dt + relativedelta(days=1)

        child1 = ParticipantNote.objects.get(
            subject_identifier=self.caregiver_child_consent.subject_identifier)

        child2 = ParticipantNote.objects.get(
            subject_identifier=caregiver_child_consent.subject_identifier)

        self.assertEqual(child1.date, rescheduled_dt.date())
        self.assertEqual(child2.date, booking_dt.date())

    @tag('sans')
    def test_sec_aims_not_scheduled(self):
        self.maternal_dataset_options.update(
            study_maternal_identifier='4321',
            protocol='Mashi',
            delivdt=get_utcnow() - relativedelta(years=11),
            preg_pi=1, )
        self.child_dataset_options.update(
            infant_hiv_exposed='exposed', study_maternal_identifier='4321',
            study_child_identifier='2314')

        child_dataset = mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=11),
            **self.child_dataset_options)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.flourishconsentversion',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            version=app_config.consent_version,
            child_version=app_config.consent_version)

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier, )

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=NOT_APPLICABLE,
            biological_caregiver=YES,
            **self.options)

        caregiver_child_consent_obj = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            gender=MALE,
            study_child_identifier=child_dataset.study_child_identifier,
            child_dob=maternal_dataset_obj.delivdt.date(), )

        child_assent = mommy.make_recipe(
            'flourish_child.childassent',
            subject_identifier=caregiver_child_consent_obj.subject_identifier,
            first_name=caregiver_child_consent_obj.first_name,
            last_name=caregiver_child_consent_obj.last_name,
            dob=caregiver_child_consent_obj.child_dob,
            identity=caregiver_child_consent_obj.identity,
            confirm_identity=caregiver_child_consent_obj.identity,
            remain_in_study=YES,
            version=subject_consent.version)

        mommy.make_recipe(
            'flourish_caregiver.caregiverpreviouslyenrolled',
            subject_identifier=subject_consent.subject_identifier)

        self.assertEqual(OnScheduleChildCohortCSec.objects.filter(
            subject_identifier=child_assent.subject_identifier,
            schedule_name='child_c_sec_schedule1').count(), 1)

        self.assertEqual(ParticipantNote.objects.filter(
            subject_identifier=child_assent.subject_identifier).count(), 0)

    @skip("Only showing notification, no longer scheduling from signals")
    def test_aging_out_scheduling(self):
        """ Assert child enrolled 5months prior aging out of their cohort
            is scheduled for follow-up before they age up.
        """
        child_dataset_options = {
            'infant_hiv_exposed': 'Exposed',
            'infant_enrolldate': get_utcnow().date(),
            'study_maternal_identifier': '12345',
            'study_child_identifier': '1235',
            'infant_sex': MALE
        }

        child_dataset = mommy.make_recipe(
            'flourish_child.childdataset',
            dob=(get_utcnow() - relativedelta(years=4, months=5)).date(),
            **child_dataset_options)

        caregiver_child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=self.subject_consent,
            gender=MALE,
            study_child_identifier=child_dataset.study_child_identifier,
            child_dob=child_dataset.dob, )

        self.assertEqual(OnScheduleChildCohortAEnrollment.objects.filter(
            subject_identifier=caregiver_child_consent.subject_identifier).count(), 1)

        booked_date = (get_utcnow() + relativedelta(months=7)).date()
        self.assertEqual(ParticipantNote.objects.filter(
            subject_identifier=caregiver_child_consent.subject_identifier,
            date=booked_date).count(), 1)
