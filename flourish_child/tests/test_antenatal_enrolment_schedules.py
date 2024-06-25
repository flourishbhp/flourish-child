from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.test import tag, TestCase
from edc_appointment.models import Appointment as CaregiverAppointment
from edc_base import get_utcnow
from edc_constants.constants import NEG, YES
from edc_facility.import_holidays import import_holidays
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy

from flourish_child.models import ChildDummySubjectConsent, \
    OnScheduleChildCohortABirth, OnScheduleChildCohortAEnrollment

app_config = django_apps.get_app_config('flourish_child')


@tag('aaeas')
class TestAntenatalEnrolmentSchedules(TestCase):
    def setUp(self):
        import_holidays()

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': app_config.consent_version
        }

        self.screening_preg = mommy.make_recipe(
            'flourish_caregiver.screeningpregwomen',
        )

        self.preg_subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=self.screening_preg.screening_identifier,
            breastfeed_intent=YES,
            **self.options)

        self.preg_caregiver_child_consent_obj = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=self.preg_subject_consent,
            gender=None,
            first_name=None,
            last_name=None,
            identity=None,
            confirm_identity=None,
            study_child_identifier=None,
            child_dob=None,
            version='2')

        self.preg_subject_identifier = self.preg_subject_consent.subject_identifier

        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            current_hiv_status=NEG,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        caregiver_visit = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=CaregiverAppointment.objects.get(
                subject_identifier=self.preg_subject_consent.subject_identifier,
                visit_code='1000M'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_caregiver.ultrasound',
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            maternal_visit=caregiver_visit, )

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            subject_identifier=self.preg_subject_consent.subject_identifier,
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            delivery_datetime=get_utcnow(),
            live_infants_to_register=1)

        mommy.make_recipe(
            'flourish_child.childbirth',
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            dob=(get_utcnow() - relativedelta(days=1)).date(),
            user_created='imosweu')

        child_consent = ChildDummySubjectConsent.objects.get(
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
        )

        child_consent.dob = (get_utcnow() - relativedelta(days=1)).date()
        child_consent.save_base(raw=True)

    @tag('aaeas')
    def test_enrol_right_schedules(self):
        self.assertEqual(OnScheduleChildCohortABirth.objects.filter(
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            schedule_name='child_a_birth_schedule1').count(), 1)

        self.assertEqual(OnScheduleChildCohortAEnrollment.objects.filter(
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            schedule_name='child_a_enrol_schedule1').count(), 0)
