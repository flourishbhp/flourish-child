from dateutil.relativedelta import relativedelta
from django.test import tag, TestCase
from edc_appointment.models import Appointment as CaregiverAppointment
from edc_base import get_utcnow
from edc_constants.constants import MALE, PENDING, POS, YES
from edc_facility.import_holidays import import_holidays
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata.models import CrfMetadata
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy

from flourish_child.models import Appointment, ChildDummySubjectConsent, \
    ChildHIVTestVisits, InfantHIVTesting, OnScheduleChildCohortAQuarterly


@tag('hiv_infant_testing')
class TestHivInfantTesting(TestCase):
    def setUp(self):
        import_holidays()

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '4'
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
            version='4')

        self.preg_subject_identifier = self.preg_subject_consent.subject_identifier

        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            current_hiv_status=POS,
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
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
            delivery_datetime=get_utcnow() - relativedelta(years=1, months=3),
            live_infants_to_register=1)

        mommy.make_recipe(
            'flourish_child.childbirth',
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            dob=(get_utcnow() - relativedelta(years=1, months=3)).date(),
            user_created='imosweu')

        child_consent = ChildDummySubjectConsent.objects.get(
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
        )

        child_consent.dob = (get_utcnow() - relativedelta(days=1)).date()
        child_consent.save_base(raw=True)

    def test_hiv_infant_testing_required(self):
        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2000D'),
            is_present=YES,
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(OnScheduleChildCohortAQuarterly.objects.filter(
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            schedule_name='child_a_quart_schedule1').count(), 1)

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                visit_code='2001',
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_child.infanthivtesting',
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            visit_code='2001').entry_status, REQUIRED)

    def test_hiv_infant_testing_required_not_required_prior_part(self):
        marternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            delivdt=get_utcnow() - relativedelta(years=1, months=6),
            **self.maternal_dataset_options)

        child_dataset = mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=1, months=6),
            **self.child_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=marternal_dataset_obj.screening_identifier,
        )

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=marternal_dataset_obj.screening_identifier,
            breastfeed_intent=YES,
            biological_caregiver=YES,
            **self.options)

        caregiver_child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=child_dataset.study_child_identifier,
            child_dob=marternal_dataset_obj.delivdt.date(), )

        mommy.make_recipe(
            'flourish_caregiver.caregiverpreviouslyenrolled',
            subject_identifier=subject_consent.subject_identifier)

        self.assertEqual(ChildDummySubjectConsent.objects.filter(
            identity=caregiver_child_consent.identity).count(), 1)

        dummy_consent = ChildDummySubjectConsent.objects.get(
            subject_identifier=caregiver_child_consent.subject_identifier)

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

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                visit_code='2001',
                subject_identifier=caregiver_child_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_child.infanthivtesting',
            subject_identifier=caregiver_child_consent.subject_identifier,
            visit_code='2001').entry_status, NOT_REQUIRED)

    @tag('ihtb')
    def test_infant_hiv_testing_birth(self):
        visit = self.create_2000_2001_visits()

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_child.infanthivtestingbirth',
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            visit_code='2001').entry_status, NOT_REQUIRED)

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_child.infanthivtestingafterbreastfeeding',
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            visit_code='2001').entry_status, NOT_REQUIRED)

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_child.infanthivtesting18months',
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            visit_code='2001').entry_status, NOT_REQUIRED)

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_child.infanthivtestingage6to8weeks',
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            visit_code='2001').entry_status, NOT_REQUIRED)

        self.create_test_visit(visit=visit)

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_child.infanthivtestingbirth',
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            visit_code='2001').entry_status, REQUIRED)

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_child.infanthivtestingafterbreastfeeding',
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            visit_code='2001').entry_status, REQUIRED)

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_child.infanthivtesting18months',
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            visit_code='2001').entry_status, REQUIRED)

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_child.infanthivtestingage6to8weeks',
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            visit_code='2001').entry_status, REQUIRED)

    @tag('ihtrp')
    def test_infant_hiv_testing_results_pending(self):
        visit = self.create_2000_2001_visits()
        self.create_test_visit(visit=visit)

        mommy.make_recipe(
            'flourish_child.infanthivtestingafterbreastfeeding',
            child_visit=visit,
            report_datetime=get_utcnow(),
            hiv_test_result=PENDING
        )

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                visit_code='2001',
                visit_code_sequence=1,
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier),
            is_present=YES,
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_child.infanthivtestingafterbreastfeeding',
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            visit_code_sequence=1,
            visit_code='2001').entry_status, REQUIRED)

    def create_test_visit(self, visit):
        options = ['after_breastfeeding', '18_months', '6_to_8_weeks', '9_months',
                   'birth']
        option_list = []
        for option in options:
            _option = ChildHIVTestVisits.objects.create(
                name=option,
                short_name=option,
                display_index=1, )
            option_list.append(_option)

        hiv_test = mommy.make_recipe(
            'flourish_child.infanthivtesting',
            child_visit=visit,
            report_datetime=get_utcnow(),
        )
        hiv_test = InfantHIVTesting.objects.get(child_visit=visit)

        for option in option_list:
            hiv_test.test_visit.add(option)
        hiv_test.save()

    def create_2000_2001_visits(self):
        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                visit_code='2000D',
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier),
            is_present=YES,
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        visit = mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                visit_code='2001',
                visit_code_sequence=0,
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        return visit
