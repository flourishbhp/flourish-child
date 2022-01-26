from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, POS, NEG
from edc_facility.import_holidays import import_holidays
from edc_metadata.constants import REQUIRED, NOT_REQUIRED
from edc_metadata.models import CrfMetadata
from model_mommy import mommy

from edc_visit_tracking.constants import SCHEDULED
from flourish_child.models.child_visit import ChildVisit

from ..models import Appointment


@tag('cohorta')
class TestRuleGroups(TestCase):

    def setUp(self):
        import_holidays()

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '2'}

        screening_preg = mommy.make_recipe(
            'flourish_caregiver.screeningpregwomen',)

        self.preg_subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=screening_preg.screening_identifier,
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

    @tag('bdt')
    def test_birthdata_required(self):
        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            current_hiv_status=NEG,
            subject_identifier=self.preg_subject_consent.subject_identifier,)

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            subject_identifier=self.preg_subject_consent.subject_identifier,
            delivery_datetime=get_utcnow(),
            live_infants_to_register=1)

        mommy.make_recipe(
            'flourish_child.childbirth',
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            dob=(get_utcnow() - relativedelta(days=1)).date(),)

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_subject_identifier,
                visit_code='2000D'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.birthdata',
                subject_identifier=self.preg_subject_identifier,
                visit_code='2000D').entry_status, REQUIRED)

    @tag('fsc')
    def test_foodsecquestionnaire_not_required(self):

        maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=2, months=5),
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-infected',
            'study_maternal_identifier': '89721',
            'protocol': 'Tshilo Dikotla'}

        child_dataset_options = {
            'infant_hiv_exposed': 'Exposed',
            'infant_enrolldate': get_utcnow(),
            'study_maternal_identifier': '89721',
            'study_child_identifier': '1234'}

        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=10, months=2),
            **child_dataset_options)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            **maternal_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=YES,
            **self.options)

        caregiver_child_consent_obj = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            version='2')

        mommy.make_recipe(
                'flourish_caregiver.caregiverpreviouslyenrolled',
                subject_identifier=subject_consent.subject_identifier)

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=caregiver_child_consent_obj.subject_identifier,
                visit_code='2000'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.childfoodsecurityquestionnaire',
                subject_identifier=caregiver_child_consent_obj.subject_identifier,
                visit_code='2000').entry_status, NOT_REQUIRED)

    @tag('fsc1')
    def test_foodsecquestionnaire_required(self):
        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            current_hiv_status=NEG,
            subject_identifier=self.preg_subject_consent.subject_identifier,)

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            subject_identifier=self.preg_subject_consent.subject_identifier,
            live_infants_to_register=1)

        mommy.make_recipe(
            'flourish_child.childbirth',
            subject_identifier=self.preg_subject_consent.subject_identifier,
            dob=(get_utcnow() - relativedelta(months=36)).date(),)

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.subject_identifier,
                visit_code='2000D'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.childfoodsecurityquestionnaire',
                subject_identifier=self.subject_identifier,
                visit_code='2000D').entry_status, NOT_REQUIRED)

    def test_arv_exposure_required_if_pos(self):
        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            current_hiv_status=POS,
            subject_identifier=self.preg_subject_consent.subject_identifier,)

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            subject_identifier=self.preg_subject_consent.subject_identifier,)

        mommy.make_recipe(
            'flourish_child.childbirth',
            subject_identifier=self.preg_subject_consent.subject_identifier,
            dob=(get_utcnow() - relativedelta(days=1)).date(),)

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.subject_identifier,
                visit_code='2000D'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.infantarvexposure',
                subject_identifier=self.subject_identifier,
                visit_code='2000D',
                visit_code_sequence='0').entry_status, REQUIRED)

    def test_arv_exposure_not_required_if_neg(self):
        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            current_hiv_status=NEG,
            subject_identifier=self.preg_subject_consent.subject_identifier,)

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            subject_identifier=self.preg_subject_consent.subject_identifier,)

        mommy.make_recipe(
            'flourish_child.childbirth',
            subject_identifier=self.preg_subject_consent.subject_identifier,
            dob=(get_utcnow() - relativedelta(days=1)).date(),)

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.subject_identifier,
                visit_code='2000D'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.infantarvexposure',
                subject_identifier=self.subject_identifier,
                visit_code='2000D',
                visit_code_sequence='0').entry_status, NOT_REQUIRED)
