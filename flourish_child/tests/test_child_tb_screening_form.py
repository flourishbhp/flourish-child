from dateutil.relativedelta import relativedelta
from django.test import tag, TestCase
from edc_base import get_utcnow
from edc_constants.constants import MALE, PENDING, YES
from edc_facility.import_holidays import import_holidays
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata.models import CrfMetadata
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy

from flourish_child.models import Appointment


@tag('ctbsf')
class TestChildTbScreeningForm(TestCase):

    def setUp(self):
        import_holidays()
        self.study_maternal_identifier = '1234'
        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '1'}

        self.maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=12, months=5),
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-infected',
            'study_maternal_identifier': self.study_maternal_identifier,
            'protocol': 'Tshilo Dikotla'}

        self.child_dataset_options = {
            'infant_hiv_exposed': 'Exposed',
            'infant_enrolldate': get_utcnow(),
            'study_maternal_identifier': self.study_maternal_identifier,
            'study_child_identifier': '1234'}

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=12, months=5),
            **self.child_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier, )

        self.subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=YES,
            **self.options)

        self.caregiver_child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=self.subject_consent,
            gender=MALE,
            study_child_identifier=self.child_dataset_options['study_child_identifier'],
            child_dob=maternal_dataset_obj.delivdt.date(), )

        mommy.make_recipe(
            'flourish_child.childassent',
            subject_identifier=self.caregiver_child_consent.subject_identifier,
            first_name=self.caregiver_child_consent.first_name,
            last_name=self.caregiver_child_consent.last_name,
            dob=self.caregiver_child_consent.child_dob,
            identity=self.caregiver_child_consent.identity,
            confirm_identity=self.caregiver_child_consent.identity,
            remain_in_study=YES,
            version=self.caregiver_child_consent.version)

        mommy.make_recipe(
            'flourish_caregiver.caregiverpreviouslyenrolled',
            subject_identifier=self.subject_consent.subject_identifier)

        self.child_visit = mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                visit_code='2000',
                subject_identifier=self.caregiver_child_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.child_visit_2001 = mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                visit_code='2001',
                subject_identifier=self.caregiver_child_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

    def test_child_tb_screening_form_required(self):

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_child.childtbscreening',
            subject_identifier=self.child_visit_2001.subject_identifier,
            visit_code='2001').entry_status, REQUIRED)

        mommy.make_recipe(
            'flourish_child.childtbscreening',
            child_visit=self.child_visit_2001,
            report_datetime=get_utcnow(),
            chest_xray_results=PENDING, )

        child_visit_2002 = mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                visit_code='2002',
                subject_identifier=self.caregiver_child_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_child.childtbscreening',
            subject_identifier=child_visit_2002.subject_identifier,
            visit_code='2002').entry_status, REQUIRED)
