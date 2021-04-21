from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import NOT_APPLICABLE, YES
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy

from ..models import OnScheduleChildCohortAEnrollment, OnScheduleChildCohortABirth
from ..models import OnScheduleChildCohortAQuarterly, OnScheduleChildCohortBEnrollment
from ..models import OnScheduleChildCohortBQuarterly, OnScheduleChildCohortCEnrollment
from ..models import OnScheduleChildCohortCQuarterly, OnScheduleChildCohortCPool
from ..models import ChildDummySubjectConsent, Appointment


@tag('cvs')
class TestVisitScheduleSetup(TestCase):

    def setUp(self):
        import_holidays()
        self.maternal_subject_identifier = '12345678'

        self.options = {
            'consent_datetime': get_utcnow(),
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

    # def test_cohort_a_onschedule_antenatal_valid(self):
    #
        # screening_preg = mommy.make_recipe(
            # 'flourish_caregiver.screeningpregwomen',)
            #
        # subject_consent = mommy.make_recipe(
            # 'flourish_caregiver.subjectconsent',
            # screening_identifier=screening_preg.screening_identifier,
            # subject_identifier=self.maternal_subject_identifier,
            # breastfeed_intent=YES,
            # **self.options)
            #
        # mommy.make_recipe(
            # 'flourish_caregiver.antenatalenrollment',
            # subject_identifier=subject_consent.subject_identifier,)
            #
        # maternal_delivery = mommy.make_recipe(
            # 'flourish_caregiver.maternaldelivery',
            # subject_identifier=subject_consent.subject_identifier,)
            #
        # dummy_consent = ChildDummySubjectConsent.objects.get(
            # consent_datetime=maternal_delivery.delivery_datetime)
            #
        # self.assertEqual(OnScheduleChildCohortAEnrollment.objects.filter(
            # subject_identifier=dummy_consent.subject_identifier,
            # schedule_name='child_a_enrol_schedule1').count(), 1)
            #
        # self.assertEqual(OnScheduleChildCohortABirth.objects.filter(
            # subject_identifier=dummy_consent.subject_identifier,
            # schedule_name='child_a_birth_schedule1').count(), 1)
            #
        # self.assertEqual(OnScheduleChildCohortAQuarterly.objects.filter(
            # subject_identifier=dummy_consent.subject_identifier,
            # schedule_name='child_a_quart_schedule1').count(), 1)

    def test_cohort_a_onschedule_consent_valid(self):
        self.maternal_subject_identifier = self.maternal_subject_identifier[:-1] + '1'

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.maternal_subject_identifier,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            subject_identifier=self.maternal_subject_identifier + '10',
            dob=get_utcnow() - relativedelta(years=2, months=5),
            **self.child_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            subject_identifier=self.maternal_subject_identifier,
            breastfeed_intent=YES,
            ** self.options)

        caregiver_child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            child_dob=(get_utcnow() - relativedelta(years=2, months=5)).date(),)

        self.assertEqual(ChildDummySubjectConsent.objects.filter(
            identity=caregiver_child_consent.identity).count(), 1)

        dummy_consent = ChildDummySubjectConsent.objects.get(
            identity=caregiver_child_consent.identity)

        self.assertEqual(OnScheduleChildCohortAEnrollment.objects.filter(
            subject_identifier=dummy_consent.subject_identifier,
            schedule_name='child_a_enrol_schedule1').count(), 1)

        self.assertEqual(OnScheduleChildCohortAQuarterly.objects.filter(
            subject_identifier=dummy_consent.subject_identifier,
            schedule_name='child_a_quart_schedule1').count(), 1)

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
            dob=get_utcnow() - relativedelta(years=5, months=2),
            **self.child_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=NOT_APPLICABLE,
            **self.options)

        caregiver_child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            child_dob=(get_utcnow() - relativedelta(years=5, months=2)).date(),)

        dummy_consent = ChildDummySubjectConsent.objects.get(
            identity=caregiver_child_consent.identity)

        self.assertEqual(OnScheduleChildCohortBEnrollment.objects.filter(
            subject_identifier=dummy_consent.subject_identifier,
            schedule_name='child_b_enrol_schedule1').count(), 1)

        self.assertEqual(OnScheduleChildCohortBQuarterly.objects.filter(
            subject_identifier=dummy_consent.subject_identifier,
            schedule_name='child_b_quart_schedule1').count(), 1)

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
            dob=get_utcnow() - relativedelta(years=7, months=2),
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
            breastfeed_intent=NOT_APPLICABLE,
            **self.options)

        caregiver_child_consent_obj = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            child_dob=(get_utcnow() - relativedelta(years=7, months=2)).date(),)

        child_assent = mommy.make_recipe(
            'flourish_child.childassent',
            subject_identifier=caregiver_child_consent_obj.subject_identifier,
            dob=get_utcnow() - relativedelta(years=7, months=2),
            identity=caregiver_child_consent_obj.identity,
            confirm_identity=caregiver_child_consent_obj.identity,
            version=subject_consent.version)

        dummy_consent = ChildDummySubjectConsent.objects.get(
            identity=child_assent.identity)

        self.assertEqual(OnScheduleChildCohortBEnrollment.objects.filter(
            subject_identifier=dummy_consent.subject_identifier,
            schedule_name='child_b_enrol_schedule1').count(), 1)

        self.assertEqual(OnScheduleChildCohortBQuarterly.objects.filter(
            subject_identifier=dummy_consent.subject_identifier,
            schedule_name='child_b_quart_schedule1').count(), 1)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=dummy_consent.subject_identifier).count(), 0)

    def test_cohort_c_onschedule_valid(self):
        self.maternal_subject_identifier = self.maternal_subject_identifier[:-1] + '3'

        self.maternal_dataset_options['protocol'] = 'Mashi'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=10,
                                                                                months=2)
        self.maternal_dataset_options['preg_pi'] = 1
        self.child_dataset_options['infant_hiv_exposed'] = 'Unexposed'
        self.options['subject_identifier'] = self.maternal_subject_identifier

        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=10, months=2),
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
            breastfeed_intent=NOT_APPLICABLE,
            **self.options)

        caregiver_child_consent_obj = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            identity='126513789',
            confirm_identity='126513789',
            child_dob=(get_utcnow() - relativedelta(years=10, months=2)).date(),)

        child_assent = mommy.make_recipe(
            'flourish_child.childassent',
            subject_identifier=caregiver_child_consent_obj.subject_identifier,
            dob=get_utcnow() - relativedelta(years=10, months=2),
            identity=caregiver_child_consent_obj.identity,
            confirm_identity=caregiver_child_consent_obj.identity,
            version=subject_consent.version)

        dummy_consent = ChildDummySubjectConsent.objects.get(
            identity=child_assent.identity)

        self.assertEqual(OnScheduleChildCohortCEnrollment.objects.filter(
            subject_identifier=dummy_consent.subject_identifier,
            schedule_name='child_c_enrol_schedule1').count(), 1)

        self.assertEqual(OnScheduleChildCohortCQuarterly.objects.filter(
            subject_identifier=dummy_consent.subject_identifier,
            schedule_name='child_c_quart_schedule1').count(), 1)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=dummy_consent.subject_identifier).count(), 0)

    @tag('cvs1')
    def test_cohort_c_twins_onschedule_valid(self):
        self.maternal_subject_identifier = self.maternal_subject_identifier[:-1] + '4'

        self.maternal_dataset_options['protocol'] = 'Mashi'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=10,
                                                                                months=2)
        self.maternal_dataset_options['preg_pi'] = 1
        self.child_dataset_options['infant_hiv_exposed'] = 'Unexposed'
        self.options['subject_identifier'] = self.maternal_subject_identifier

        mommy.make_recipe(
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
            subject_identifier=self.maternal_subject_identifier,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=NOT_APPLICABLE,
            **self.options)

        caregiver_child_consent_obj1 = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            identity='126513789',
            confirm_identity='126513789',
            child_dob=(get_utcnow() - relativedelta(years=10, months=2)).date(),)

        caregiver_child_consent_obj2 = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            identity='126516789',
            confirm_identity='126516789',
            child_dob=(get_utcnow() - relativedelta(years=10, months=2)).date(),)

        child_assent1 = mommy.make_recipe(
            'flourish_child.childassent',
            subject_identifier=caregiver_child_consent_obj1.subject_identifier,
            dob=get_utcnow() - relativedelta(years=10, months=2),
            identity=caregiver_child_consent_obj1.identity,
            confirm_identity=caregiver_child_consent_obj1.identity,
            version=subject_consent.version)

        child_assent2 = mommy.make_recipe(
            'flourish_child.childassent',
            subject_identifier=caregiver_child_consent_obj2.subject_identifier,
            dob=get_utcnow() - relativedelta(years=10, months=2),
            identity=caregiver_child_consent_obj2.identity,
            confirm_identity=caregiver_child_consent_obj2.identity,
            version=subject_consent.version)

        dummy_consent1 = ChildDummySubjectConsent.objects.get(
            identity=child_assent1.identity)

        dummy_consent2 = ChildDummySubjectConsent.objects.get(
            identity=child_assent2.identity)

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
