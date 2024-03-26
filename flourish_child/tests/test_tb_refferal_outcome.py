from dateutil.relativedelta import relativedelta
from django.test import tag, TestCase
from edc_base import get_utcnow
from edc_constants.constants import MALE, NO, YES
from edc_facility.import_holidays import import_holidays
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata.models import CrfMetadata
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy

from flourish_child.models import Appointment


@tag('ctbro')
class TestTBReferralOutcome(TestCase):

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

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            delivdt=get_utcnow() - relativedelta(years=3, months=0),
            **self.maternal_dataset_options)

        child_dataset = mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=3, months=0),
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

        self.caregiver_child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=child_dataset.study_child_identifier,
            child_dob=maternal_dataset_obj.delivdt.date(), )

        mommy.make_recipe(
            'flourish_caregiver.caregiverpreviouslyenrolled',
            subject_identifier=subject_consent.subject_identifier)

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.caregiver_child_consent.subject_identifier,
                visit_code='2000'),
            is_present=YES,
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.child_visit_2001 = mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                visit_code='2001',
                subject_identifier=self.caregiver_child_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

    def test_tb_referral_outcome_required(self):
        self.assertEqual(CrfMetadata.objects.get(
            subject_identifier=self.caregiver_child_consent.subject_identifier,
            model='flourish_child.childtbreferraloutcome',
            visit_code='2001').entry_status, NOT_REQUIRED)

        mommy.make_recipe(
            'flourish_child.childtbreferral',
            child_visit=self.child_visit_2001,
        )

        self.assertEqual(CrfMetadata.objects.get(
            subject_identifier=self.caregiver_child_consent.subject_identifier,
            model='flourish_child.childtbreferraloutcome',
            visit_code='2001').entry_status, REQUIRED)

    def test_tb_referral_outcome_not_required(self):
        self.assertEqual(CrfMetadata.objects.get(
            subject_identifier=self.caregiver_child_consent.subject_identifier,
            model='flourish_child.childtbreferraloutcome',
            visit_code='2001').entry_status, NOT_REQUIRED)

        mommy.make_recipe(
            'flourish_child.childtbreferral',
            child_visit=self.child_visit_2001,
        )

        self.assertEqual(CrfMetadata.objects.get(
            subject_identifier=self.caregiver_child_consent.subject_identifier,
            model='flourish_child.childtbreferraloutcome',
            visit_code='2001').entry_status, NOT_REQUIRED)
