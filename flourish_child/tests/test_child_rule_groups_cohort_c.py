from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.test import tag, TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import NO, NOT_APPLICABLE, YES
from edc_facility.import_holidays import import_holidays
from edc_metadata.constants import NOT_REQUIRED, REQUIRED
from edc_metadata.models import CrfMetadata
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy

from ..models import Appointment, ChildVisit

app_config = django_apps.get_app_config('flourish_child')


@tag('crg')
class TestRuleGroups(TestCase):

    def setUp(self):
        import_holidays()

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': app_config.consent_version}

        maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=12, months=2),
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-infected',
            'study_maternal_identifier': '12345',
            'protocol': 'Mashi',
            'preg_pi': 1}

        child_dataset_options = {
            'infant_hiv_exposed': 'Unexposed',
            'infant_enrolldate': get_utcnow(),
            'study_maternal_identifier': '12345',
            'study_child_identifier': '1234'}

        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=12, months=2),
            **child_dataset_options)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            **maternal_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.flourishconsentversion',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            version=app_config.consent_version,
            child_version=app_config.consent_version)

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier, )

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=NOT_APPLICABLE,
            **self.options)

        caregiver_child_consent_obj = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=child_dataset_options.get(
                'study_child_identifier'),
            identity='126513789',
            confirm_identity='126513789',
            child_dob=(get_utcnow() -
                       relativedelta(years=12, months=2)).date(),
            version=app_config.consent_version)

        mommy.make_recipe(
            'flourish_caregiver.caregiverpreviouslyenrolled',
            subject_identifier=subject_consent.subject_identifier)

        mommy.make_recipe(
            'flourish_child.childassent',
            subject_identifier=caregiver_child_consent_obj.subject_identifier,
            dob=(get_utcnow() - relativedelta(years=12, months=2)).date(),
            identity=caregiver_child_consent_obj.identity,
            confirm_identity=caregiver_child_consent_obj.identity,
            version=subject_consent.version)

        self.subject_identifier = caregiver_child_consent_obj.subject_identifier

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.subject_identifier,
                visit_code='2000'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

    def test_academic_performance_required(self):
        visit = ChildVisit.objects.get(visit_code='2000')
        mommy.make_recipe('flourish_child.childsociodemographic',
                          child_visit=visit)
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.academicperformance',
                subject_identifier=self.subject_identifier,
                visit_code='2000').entry_status, REQUIRED)

    def test_academic_performance_not_required(self):
        visit = ChildVisit.objects.get(visit_code='2000')
        mommy.make_recipe('flourish_child.childsociodemographic',
                          child_visit=visit,
                          attend_school=NO)
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.academicperformance',
                subject_identifier=self.subject_identifier,
                visit_code='2000').entry_status, NOT_REQUIRED)

    def test_gad_score_gte10_referral_required(self):
        visit = ChildVisit.objects.get(visit_code='2000')
        mommy.make_recipe('flourish_child.childgadanxietyscreening',
                          child_visit=visit)
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.childgadreferral',
                subject_identifier=self.subject_identifier,
                visit_code='2000').entry_status, REQUIRED)

    def test_gad_score_lte10_referral_not_required(self):
        visit = ChildVisit.objects.get(visit_code='2000')
        mommy.make_recipe('flourish_child.childgadanxietyscreening',
                          feeling_anxious='0',
                          control_worrying='0',
                          fearful='0',
                          child_visit=visit)
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.childgadreferral',
                subject_identifier=self.subject_identifier,
                visit_code='2000').entry_status, NOT_REQUIRED)

    def test_phq9_gte10_referral_required(self):
        visit = ChildVisit.objects.get(visit_code='2000')
        mommy.make_recipe('flourish_child.childphqdeprscreening',
                          child_visit=visit)
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.childphqreferral',
                subject_identifier=self.subject_identifier,
                visit_code='2000').entry_status, REQUIRED)

    def test_phq9_suicide_attmptyes_referral_required(self):
        visit = ChildVisit.objects.get(visit_code='2000')
        mommy.make_recipe('flourish_child.childphqdeprscreening',
                          self_harm='0',
                          suidice_attempt=YES,
                          child_visit=visit)
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.childphqreferral',
                subject_identifier=self.subject_identifier,
                visit_code='2000').entry_status, REQUIRED)



