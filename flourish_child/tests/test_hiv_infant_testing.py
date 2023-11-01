from dateutil.relativedelta import relativedelta
from django.test import TestCase,tag
from edc_base import get_utcnow
from edc_constants.constants import MALE, NEG, POS, YES
from edc_facility.import_holidays import import_holidays
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata.models import CrfMetadata
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy

from flourish_child.models import Appointment, ChildDummySubjectConsent, \
    OnScheduleChildCohortAQuarterly


@tag('hiv_infant_testing')
class TestHivInfantTesting(TestCase):
    def setUp(self):
        import_holidays()

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

        self.screening_preg = mommy.make_recipe(
            'flourish_caregiver.screeningpregwomen',
        )

        self.preg_subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=self.screening_preg.screening_identifier,
            breastfeed_intent=YES,
            **self.options)

    def test_hiv_infant_testing_required(self):
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
            current_hiv_status=POS,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            subject_identifier=self.preg_subject_consent.subject_identifier,
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

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
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
                subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier),
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
