from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import NOT_APPLICABLE, YES
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy

from ..models import ChildDummySubjectConsent, Appointment
from ..models import OnScheduleChildCohortAEnrollment, OnScheduleChildCohortABirth
from ..models import OnScheduleChildCohortAQuarterly, OnScheduleChildCohortBEnrollment
from ..models import OnScheduleChildCohortASec, OnScheduleChildCohortBSec, OnScheduleChildCohortCSec
from ..models import OnScheduleChildCohortBQuarterly, OnScheduleChildCohortCEnrollment
from ..models import OnScheduleChildCohortCQuarterly, OnScheduleChildCohortCPool


@tag('cvs')
class TestVisitScheduleSetup(TestCase):

    def setUp(self):
        import_holidays()

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '1'}

        self.maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=2, months=0),
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-infected',
            'study_maternal_identifier': '12345',
            'protocol': 'Tshilo Dikotla'}

        self.child_dataset_options = {
            'infant_hiv_exposed': 'Exposed',
            'infant_enrolldate': get_utcnow(),
            'study_maternal_identifier': '12345',
            'study_child_identifier': '1234'}

    def year_3_age(self, year_3_years, year_3_months):
        """Returns the age at year 3.
        """
        app_config = django_apps.get_app_config('flourish_caregiver')
        start_date_year_3 = app_config.start_date_year_3

        child_dob = start_date_year_3 - relativedelta(years=year_3_years,
                                                      months=year_3_months)
        return child_dob

    @tag('cvs0')
    def test_cohort_a_onschedule_consent_valid(self):
        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            **self.maternal_dataset_options)

        child_dataset = mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=2, months=0),
            **self.child_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=YES,
            biological_caregiver=YES,
            ** self.options)

        caregiver_child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=child_dataset.study_child_identifier,
            child_dob=maternal_dataset_obj.delivdt,)

        mommy.make_recipe(
                'flourish_caregiver.caregiverpreviouslyenrolled',
                subject_identifier=subject_consent.subject_identifier)

        self.assertEqual(ChildDummySubjectConsent.objects.filter(
            identity=caregiver_child_consent.identity).count(), 1)

        dummy_consent = ChildDummySubjectConsent.objects.get(
            subject_identifier=caregiver_child_consent.subject_identifier)

        self.assertEqual(OnScheduleChildCohortAEnrollment.objects.filter(
            subject_identifier=dummy_consent.subject_identifier,
            schedule_name='child_a_enrol_schedule1').count(), 1)

        self.assertEqual(OnScheduleChildCohortAQuarterly.objects.filter(
            subject_identifier=dummy_consent.subject_identifier,
            schedule_name='child_a_quart_schedule1').count(), 1)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=dummy_consent.subject_identifier).count(), 0)

    @tag('cvs1')
    def test_cohort_b_onschedule_valid(self):
        self.maternal_dataset_options['protocol'] = 'Mpepu'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=5,
                                                                                months=2)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            preg_efv=1,
            **self.maternal_dataset_options)

        child_dataset = mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=5, months=2),
            **self.child_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=NOT_APPLICABLE,
            biological_caregiver=YES,
            **self.options)

        caregiver_child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=child_dataset.study_child_identifier,
            child_dob=maternal_dataset_obj.delivdt)

        mommy.make_recipe(
                'flourish_caregiver.caregiverpreviouslyenrolled',
                subject_identifier=subject_consent.subject_identifier)

        dummy_consent = ChildDummySubjectConsent.objects.get(
            subject_identifier=caregiver_child_consent.subject_identifier)

        self.assertEqual(OnScheduleChildCohortBEnrollment.objects.filter(
            subject_identifier=dummy_consent.subject_identifier,
            schedule_name='child_b_enrol_schedule1').count(), 1)

        self.assertEqual(OnScheduleChildCohortBQuarterly.objects.filter(
            subject_identifier=dummy_consent.subject_identifier,
            schedule_name='child_b_quart_schedule1').count(), 1)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=dummy_consent.subject_identifier).count(), 0)

    @tag('t1')
    def test_cohort_b_assent_onschedule_valid(self):
        self.maternal_dataset_options['protocol'] = 'Mpepu'
        self.maternal_dataset_options['mom_hivstatus'] = 'HIV-uninfected'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=7,
                                                                                months=2)

        child_dataset = mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=7, months=2),
            **self.child_dataset_options)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=NOT_APPLICABLE,
            biological_caregiver=YES,
            **self.options)

        caregiver_child_consent_obj = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=child_dataset.study_child_identifier,
            child_dob=maternal_dataset_obj.delivdt,)

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

        dummy_consent = ChildDummySubjectConsent.objects.get(
            subject_identifier=child_assent.subject_identifier)

        self.assertEqual(OnScheduleChildCohortBEnrollment.objects.filter(
            subject_identifier=dummy_consent.subject_identifier,
            schedule_name='child_b_enrol_schedule1').count(), 1)

        self.assertEqual(OnScheduleChildCohortBQuarterly.objects.filter(
            subject_identifier=dummy_consent.subject_identifier,
            schedule_name='child_b_quart_schedule1').count(), 1)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=dummy_consent.subject_identifier).count(), 0)

    def test_cohort_c_onschedule_valid(self):
        self.child_dataset_options['infant_hiv_exposed'] = 'Unexposed'
        self.maternal_dataset_options['protocol'] = 'Tshipidi'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=11,
                                                                                months=2)

        child_dataset = mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=11, months=2),
            **self.child_dataset_options)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=NOT_APPLICABLE,
            biological_caregiver=YES,
            **self.options)

        caregiver_child_consent_obj = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=child_dataset.study_child_identifier,
            child_dob=maternal_dataset_obj.delivdt,
            cohort=None)

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

        dummy_consent = ChildDummySubjectConsent.objects.get(
            subject_identifier=child_assent.subject_identifier)

        self.assertEqual(OnScheduleChildCohortCEnrollment.objects.filter(
            subject_identifier=dummy_consent.subject_identifier,
            schedule_name='child_c_enrol_schedule1').count(), 1)

        self.assertEqual(OnScheduleChildCohortCQuarterly.objects.filter(
            subject_identifier=dummy_consent.subject_identifier,
            schedule_name='child_c_quart_schedule1').count(), 1)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=dummy_consent.subject_identifier).count(), 0)

    @tag('cvs3')
    def test_cohort_c_sec_onschedule_valid(self):
        self.maternal_dataset_options['preg_pi'] = 1
        self.child_dataset_options['infant_hiv_exposed'] = 'exposed'
        self.maternal_dataset_options['protocol'] = 'Mashi'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=11)

        child_dataset = mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=11),
            **self.child_dataset_options)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=NOT_APPLICABLE,
            biological_caregiver=YES,
            **self.options)

        caregiver_child_consent_obj = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=child_dataset.study_child_identifier,
            child_dob=maternal_dataset_obj.delivdt,)

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

        dummy_consent = ChildDummySubjectConsent.objects.get(
            subject_identifier=child_assent.subject_identifier)

        self.assertEqual(OnScheduleChildCohortCSec.objects.filter(
            subject_identifier=dummy_consent.subject_identifier,
            schedule_name='child_c_sec_schedule1').count(), 1)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=dummy_consent.subject_identifier).count(), 0)

    def test_cohort_c_twins_onschedule_valid(self):
        self.child_dataset_options['infant_hiv_exposed'] = 'Unexposed'
        self.maternal_dataset_options['protocol'] = 'Tshipidi'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=10,
                                                                                months=2)

        child_dataset = mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=10, months=2),
            twin_triplet=1,
            **self.child_dataset_options)

        self.child_dataset_options['study_child_identifier'] = '1235'
        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=10, months=2),
            twin_triplet=1,
            **self.child_dataset_options)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=NOT_APPLICABLE,
            biological_caregiver=YES,
            **self.options)

        caregiver_child_consent_obj1 = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=child_dataset.study_child_identifier,
            child_dob=maternal_dataset_obj.delivdt,)

        caregiver_child_consent_obj2 = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=child_dataset.study_child_identifier,
            child_dob=maternal_dataset_obj.delivdt,)

        child_assent1 = mommy.make_recipe(
            'flourish_child.childassent',
            subject_identifier=caregiver_child_consent_obj1.subject_identifier,
            first_name=caregiver_child_consent_obj1.first_name,
            last_name=caregiver_child_consent_obj1.last_name,
            dob=caregiver_child_consent_obj1.child_dob,
            identity=caregiver_child_consent_obj1.identity,
            confirm_identity=caregiver_child_consent_obj1.identity,
            remain_in_study=YES,
            version=subject_consent.version)

        child_assent2 = mommy.make_recipe(
            'flourish_child.childassent',
            subject_identifier=caregiver_child_consent_obj2.subject_identifier,
            first_name=caregiver_child_consent_obj2.first_name,
            last_name=caregiver_child_consent_obj2.last_name,
            dob=caregiver_child_consent_obj2.child_dob,
            identity=caregiver_child_consent_obj2.identity,
            confirm_identity=caregiver_child_consent_obj2.identity,
            remain_in_study=YES,
            version=subject_consent.version)

        mommy.make_recipe(
                'flourish_caregiver.caregiverpreviouslyenrolled',
                subject_identifier=subject_consent.subject_identifier)

        dummy_consent1 = ChildDummySubjectConsent.objects.get(
            subject_identifier=child_assent1.subject_identifier)

        dummy_consent2 = ChildDummySubjectConsent.objects.get(
            subject_identifier=child_assent2.subject_identifier)

        self.assertEqual(OnScheduleChildCohortCEnrollment.objects.filter(
            subject_identifier=dummy_consent1.subject_identifier,
            schedule_name='child_c_enrol_schedule1').count(), 1)

        self.assertEqual(OnScheduleChildCohortCQuarterly.objects.filter(
            subject_identifier=dummy_consent1.subject_identifier,
            schedule_name='child_c_quart_schedule1').count(), 1)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=dummy_consent1.subject_identifier).count(), 0)

        self.assertEqual(OnScheduleChildCohortCEnrollment.objects.filter(
            subject_identifier=dummy_consent2.subject_identifier,
            schedule_name='child_c_enrol_schedule1').count(), 1)

        self.assertEqual(OnScheduleChildCohortCQuarterly.objects.filter(
            subject_identifier=dummy_consent2.subject_identifier,
            schedule_name='child_c_quart_schedule1').count(), 1)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=dummy_consent2.subject_identifier).count(), 0)
