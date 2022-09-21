from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO, NOT_APPLICABLE
from edc_facility.import_holidays import import_holidays
from edc_metadata.constants import REQUIRED, NOT_REQUIRED
from edc_metadata.models import CrfMetadata, RequisitionMetadata
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy

from ..models import ChildVisit, Appointment


@tag('brg')
class TestBRuleGroups(TestCase):

    def setUp(self):
        import_holidays()

        self.options = {
            'consent_datetime': get_utcnow(),
            'hiv_testing': YES,
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
            'dob': get_utcnow() - relativedelta(years=2, months=0),
            'study_child_identifier': '1234'}

        mommy.make_recipe(
            'flourish_child.childdataset',
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
            **self.options)

        # breakpoint()

        caregiver_child_consent_obj = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=self.child_dataset_options.get('study_child_identifier'),
            identity='126513789',
            confirm_identity='126513789',
            child_dob=(get_utcnow() - relativedelta(years=2, months=0)).date(),
            version='1')

        mommy.make_recipe(
                'flourish_caregiver.caregiverpreviouslyenrolled',
                subject_identifier=subject_consent.subject_identifier)

        self.subject_identifier = caregiver_child_consent_obj.subject_identifier

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(subject_identifier=self.subject_identifier,
                                                visit_code='2000'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

    def test_dna_pcr_not_required(self):
        # visit = ChildVisit.objects.get(visit_code='2000')

        self.assertEqual(
            RequisitionMetadata.objects.get(
                model='flourish_child.childrequisition',
                subject_identifier=self.subject_identifier,
                visit_code='2000',
                panel_name='dna_pcr').entry_status, NOT_REQUIRED)
