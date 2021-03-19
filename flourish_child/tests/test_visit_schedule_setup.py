from django.apps import apps as django_apps
from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_appointment.models import Appointment
from edc_base.utils import get_utcnow
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy

from ..models import OnScheduleChildCohortA, OnScheduleChildCohortB, OnScheduleChildCohortC
from ..models import ChildDummySubjectConsent


@tag('cvs')
class TestVisitScheduleSetup(TestCase):

    def setUp(self):
        import_holidays()
        self.maternal_subject_identifier = '12345678'

        self.options = {
            'consent_datetime': get_utcnow(),
            'subject_identifier': self.maternal_subject_identifier,
            'version': '1'}

        self.maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=2, months=5),
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-infected',
            'study_maternal_identifier': '12345',
            'protocol': 'Tshilo Dikotla'}

        self.child_dataset_options = {
            'infant_hiv_exposed': 'Exposed',
            'infant_enrolldate': get_utcnow(),
            'study_maternal_identifier': '12345',
            'study_child_identifier': '1234'}

    def test_cohort_a_onschedule_antenatal_valid(self):

        screening_preg = mommy.make_recipe(
            'flourish_caregiver.screeningpregwomen',)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=screening_preg.screening_identifier,
            **self.options)

        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            subject_identifier=subject_consent.subject_identifier,)

        self.assertEqual(OnScheduleChildCohortA.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='cohort_a1_schedule1').count(), 0)

    def test_cohort_a_onschedule_consent_valid(self):
        self.maternal_subject_identifier = self.maternal_subject_identifier[:-1] + '1'
        self.options['subject_identifier'] = self.maternal_subject_identifier

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.maternal_subject_identifier,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            subject_identifier=self.maternal_subject_identifier + '10',
            **self.child_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            ** self.options)

        caregiver_child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            child_dob=(get_utcnow() - relativedelta(years=2, months=5)).date(),)

        self.assertEqual(ChildDummySubjectConsent.objects.filter(
            identity=caregiver_child_consent.identity).count(), 1)

        dummy_consent = ChildDummySubjectConsent.objects.get(
            identity=caregiver_child_consent.identity)

        self.assertEqual(OnScheduleChildCohortA.objects.filter(
            subject_identifier=dummy_consent.subject_identifier,
            schedule_name='child_cohort_a_schedule1').count(), 1)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=dummy_consent.subject_identifier).count(), 0)

    def test_cohort_b_onschedule_valid(self):

        self.maternal_subject_identifier = self.maternal_subject_identifier[:-1] + '2'
        self.maternal_dataset_options['protocol'] = 'Mpepu'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=5,
                                                                                months=2)
        self.options['subject_identifier'] = self.maternal_subject_identifier

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.maternal_subject_identifier,
            preg_efv=1,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            subject_identifier=self.maternal_subject_identifier + '10',
            **self.child_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            **self.options)

        caregiver_child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            child_dob=(get_utcnow() - relativedelta(years=5, months=2)).date(),)

        dummy_consent = ChildDummySubjectConsent.objects.get(
            identity=caregiver_child_consent.identity)

        self.assertEqual(OnScheduleChildCohortB.objects.filter(
            subject_identifier=dummy_consent.subject_identifier,
            schedule_name='child_cohort_b_schedule1').count(), 1)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=dummy_consent.subject_identifier).count(), 0)

    def test_cohort_b_assent_onschedule_valid(self):

        self.maternal_subject_identifier = self.maternal_subject_identifier[:-1] + '3'
        self.maternal_dataset_options['protocol'] = 'Mpepu'
        self.maternal_dataset_options['mom_hivstatus'] = 'HIV uninfected'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=7,
                                                                                months=2)
        self.options['subject_identifier'] = self.maternal_subject_identifier

        mommy.make_recipe(
            'flourish_child.childdataset',
            subject_identifier=self.maternal_subject_identifier + '10',
            **self.child_dataset_options)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.maternal_subject_identifier,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            **self.options)

        caregiver_child_consent_obj = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            child_dob=(get_utcnow() - relativedelta(years=7, months=2)).date(),)

        child_assent = mommy.make_recipe(
            'flourish_child.childassent',
            subject_identifier=self.maternal_subject_identifier + '-10',
            dob=get_utcnow() - relativedelta(years=7, months=2),
            identity=caregiver_child_consent_obj.identity,
            confirm_identity=caregiver_child_consent_obj.identity,
            version=subject_consent.version)

        dummy_consent = ChildDummySubjectConsent.objects.get(
            identity=child_assent.identity)

        self.assertEqual(OnScheduleChildCohortB.objects.filter(
            subject_identifier=dummy_consent.subject_identifier,
            schedule_name='child_cohort_b_schedule1').count(), 1)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=dummy_consent.subject_identifier).count(), 0)
