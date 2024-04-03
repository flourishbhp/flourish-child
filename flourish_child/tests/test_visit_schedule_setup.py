from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.test import TestCase, tag
from model_mommy import mommy
from edc_visit_schedule.models import SubjectScheduleHistory
from edc_base.utils import get_utcnow
from edc_constants.constants import NOT_APPLICABLE, YES, NO
from edc_facility.import_holidays import import_holidays
from edc_visit_schedule import site_visit_schedules
from edc_visit_tracking.constants import SCHEDULED

from ..models import ChildDummySubjectConsent, Appointment, \
    OnScheduleChildCohortCSecQuart
from ..models import OnScheduleChildCohortAEnrollment, \
    OnScheduleChildCohortABirth
from ..models import OnScheduleChildCohortAQuarterly, \
    OnScheduleChildCohortBEnrollment
from ..models import OnScheduleChildCohortBQuarterly, \
    OnScheduleChildCohortCEnrollment
from ..models import OnScheduleChildCohortCQuarterly
from ..models import OnScheduleChildCohortCSec


@tag('schedule')
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

    def test_cohort_a_onschedule_birth_valid(self):
        screening_preg = mommy.make_recipe(
            'flourish_caregiver.screeningpregwomen', )

        self.options.update(version=3)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=screening_preg.screening_identifier,
            breastfeed_intent=YES,
            biological_caregiver=YES,
            **self.options)

        child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            child_dob=None,
            first_name=None,
            last_name=None)

        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            child_subject_identifier=child_consent.subject_identifier,
            subject_identifier=subject_consent.subject_identifier,)

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            child_subject_identifier=child_consent.subject_identifier,
            subject_identifier=subject_consent.subject_identifier,
            delivery_datetime=get_utcnow(),
            live_infants_to_register=1)

        mommy.make_recipe(
            'flourish_child.childbirth',
            subject_identifier=child_consent.subject_identifier,
            dob=get_utcnow().date()
        )

        self.assertEqual(OnScheduleChildCohortABirth.objects.filter(
            subject_identifier=child_consent.subject_identifier,
            schedule_name='child_a_birth_schedule1').count(), 1)

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
            **self.options)

        caregiver_child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=child_dataset.study_child_identifier,
            child_dob=maternal_dataset_obj.delivdt.date(),)

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
            schedule_name='child_a_quart_schedule1').count(), 0)

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                visit_code='2000',
                subject_identifier=caregiver_child_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(OnScheduleChildCohortAQuarterly.objects.filter(
            subject_identifier=dummy_consent.subject_identifier,
            schedule_name='child_a_quart_schedule1').count(), 1)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=dummy_consent.subject_identifier).count(), 0)

    def test_cohort_b_onschedule_valid(self):
        self.maternal_dataset_options['protocol'] = 'Mpepu'
        self.maternal_dataset_options['mom_pregarv_strat'] = '3-drug ART'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(
            years=5,
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
            child_dob=maternal_dataset_obj.delivdt.date())

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
            schedule_name='child_b_quart_schedule1').count(), 0)

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                visit_code='2000',
                subject_identifier=caregiver_child_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(OnScheduleChildCohortBQuarterly.objects.filter(
            subject_identifier=dummy_consent.subject_identifier,
            schedule_name='child_b_quart_schedule1').count(), 1)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=dummy_consent.subject_identifier).count(), 0)

    def test_cohort_b_assent_onschedule_valid(self):
        self.maternal_dataset_options['protocol'] = 'Mpepu'
        self.maternal_dataset_options['mom_hivstatus'] = 'HIV-uninfected'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(
            years=7,
            months=2)
        self.child_dataset_options['infant_hiv_exposed'] = 'unexposed'

        child_dataset = mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=7, months=2),
            **self.child_dataset_options)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.flourishconsentversion',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            version='1',
            child_version='1')

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
            child_dob=maternal_dataset_obj.delivdt.date(),)

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
            schedule_name='child_b_quart_schedule1').count(), 0)

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                visit_code='2000',
                subject_identifier=dummy_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(OnScheduleChildCohortBQuarterly.objects.filter(
            subject_identifier=dummy_consent.subject_identifier,
            schedule_name='child_b_quart_schedule1').count(), 1)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=dummy_consent.subject_identifier).count(), 0)

    def test_cohort_c_onschedule_valid(self):
        self.child_dataset_options['infant_hiv_exposed'] = 'Unexposed'
        self.maternal_dataset_options['protocol'] = 'Tshipidi'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(
            years=11,
            months=2)

        child_dataset = mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=11, months=2),
            **self.child_dataset_options)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.flourishconsentversion',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            version='1',
            child_version='1')

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
            child_dob=maternal_dataset_obj.delivdt.date(),
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
            schedule_name='child_c_quart_schedule1').count(), 0)

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                visit_code='2000',
                subject_identifier=dummy_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(OnScheduleChildCohortCQuarterly.objects.filter(
            subject_identifier=dummy_consent.subject_identifier,
            schedule_name='child_c_quart_schedule1').count(), 1)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=dummy_consent.subject_identifier).count(), 0)

    def test_cohort_c_sec_onschedule_valid(self):
        self.maternal_dataset_options['preg_pi'] = 1
        self.child_dataset_options['infant_hiv_exposed'] = 'exposed'
        self.maternal_dataset_options['protocol'] = 'Mashi'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(
            years=11)

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
            version='1',
            child_version='1')

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
            child_dob=maternal_dataset_obj.delivdt.date(),)

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

        self.assertEqual(OnScheduleChildCohortCSecQuart.objects.filter(
            subject_identifier=dummy_consent.subject_identifier,
            schedule_name='child_c_sec_qt_schedule1').count(), 0)

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                visit_code='2000',
                subject_identifier=dummy_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(OnScheduleChildCohortCSecQuart.objects.filter(
            subject_identifier=dummy_consent.subject_identifier,
            schedule_name='child_c_sec_qt_schedule1').count(), 1)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=dummy_consent.subject_identifier).count(), 0)

    def test_cohort_c_twins_onschedule_valid(self):
        self.child_dataset_options['infant_hiv_exposed'] = 'Unexposed'
        self.maternal_dataset_options['protocol'] = 'Tshipidi'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(
            years=10,
            months=6)

        child_dataset = mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=10, months=6),
            twin_triplet=1,
            **self.child_dataset_options)

        self.child_dataset_options['study_child_identifier'] = '1235'
        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=10, months=6),
            twin_triplet=1,
            **self.child_dataset_options)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.flourishconsentversion',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            version='1',
            child_version='1')

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
            child_dob=maternal_dataset_obj.delivdt.date(),)

        caregiver_child_consent_obj2 = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=child_dataset.study_child_identifier,
            child_dob=maternal_dataset_obj.delivdt.date(),)

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
            schedule_name='child_c_quart_schedule1').count(), 0)

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                visit_code='2000',
                subject_identifier=dummy_consent1.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

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
            schedule_name='child_c_quart_schedule1').count(), 0)

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                visit_code='2000',
                subject_identifier=dummy_consent2.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(OnScheduleChildCohortCQuarterly.objects.filter(
            subject_identifier=dummy_consent2.subject_identifier,
            schedule_name='child_c_quart_schedule1').count(), 1)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=dummy_consent2.subject_identifier).count(), 0)

    def test_cohort_c_caregiver_offschedule(self):

        child_dob = get_utcnow().date() - relativedelta(years=18)

        screening_preg = mommy.make_recipe(
            'flourish_caregiver.screeningpregwomen', )

        self.options.update(version=3)

        caregiver_onschedule_model = 'flourish_caregiver.onschedulecohortcenrollment'

        child_dataset = mommy.make_recipe(
            'flourish_child.childdataset',
            dob=child_dob,
            **self.child_dataset_options)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=screening_preg.screening_identifier,
            breastfeed_intent=YES,
            biological_caregiver=YES,
            **self.options)

        caregiver_child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=child_dataset.study_child_identifier,
            child_dob=child_dob,)

        caregiver_child_consent.save()

        _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            onschedule_model=caregiver_onschedule_model,
            name='c_enrol1_schedule1'
        )

        schedule.put_on_schedule(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='c_enrol1_schedule1'
        )

        caregiver_onschedule_cls = django_apps.get_model(
            caregiver_onschedule_model)

        caregiver_onschedule_cls.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='c_enrol1_schedule1',
        ).update(child_subject_identifier=caregiver_child_consent.subject_identifier)

        _, child_schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            onschedule_model='flourish_child.onschedulechildcohortcenrollment',
            name='child_c_enrol_schedule1'
        )

        child_schedule.put_on_schedule(
            subject_identifier=caregiver_child_consent.subject_identifier,
            schedule_name='child_c_enrol_schedule1'
        )

        continued_consent = mommy.make_recipe(
            'flourish_child.childcontinuedconsent',
            subject_identifier=caregiver_child_consent.subject_identifier,
            consent_datetime=get_utcnow(),
            along_side_caregiver=NO,)

        continued_consent.save()

        is_off_schedule = SubjectScheduleHistory.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_status='offschedule',
            schedule_name='c_enrol1_schedule1'
        )

        self.assertTrue(is_off_schedule)

    def test_cohort_b_caregiver_offschedule(self):

        child_dob = get_utcnow().date() - relativedelta(years=18)

        screening_preg = mommy.make_recipe(
            'flourish_caregiver.screeningpregwomen', )

        self.options.update(version=3)

        caregiver_onschedule_model = 'flourish_caregiver.onschedulecohortbenrollment'

        child_dataset = mommy.make_recipe(
            'flourish_child.childdataset',
            dob=child_dob,
            **self.child_dataset_options)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=screening_preg.screening_identifier,
            breastfeed_intent=YES,
            biological_caregiver=YES,
            **self.options)

        caregiver_child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=child_dataset.study_child_identifier,
            child_dob=child_dob,)

        caregiver_child_consent.save()

        _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            onschedule_model=caregiver_onschedule_model,
            name='b_enrol1_schedule1'
        )

        schedule.put_on_schedule(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_enrol1_schedule1'
        )

        caregiver_onschedule_cls = django_apps.get_model(
            caregiver_onschedule_model)

        caregiver_onschedule_cls.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_enrol1_schedule1',
        ).update(child_subject_identifier=caregiver_child_consent.subject_identifier)

        _, child_schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            onschedule_model='flourish_child.onschedulechildcohortbenrollment',
            name='child_b_enrol_schedule1'
        )

        child_schedule.put_on_schedule(
            subject_identifier=caregiver_child_consent.subject_identifier,
            schedule_name='child_c_enrol_schedule1'
        )

        continued_consent = mommy.make_recipe(
            'flourish_child.childcontinuedconsent',
            subject_identifier=caregiver_child_consent.subject_identifier,
            consent_datetime=get_utcnow(),
            along_side_caregiver=NO,)

        continued_consent.save()

        is_off_schedule = SubjectScheduleHistory.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_status='offschedule',
            schedule_name='b_enrol1_schedule1'
        )

        self.assertTrue(is_off_schedule)