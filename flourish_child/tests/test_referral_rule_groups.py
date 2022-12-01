from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import NOT_APPLICABLE, YES
from edc_facility.import_holidays import import_holidays
from edc_metadata.constants import REQUIRED, NOT_REQUIRED
from edc_metadata.models import CrfMetadata
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy

from ..models import Appointment, ChildVisit, ChildDummySubjectConsent


@tag('creff')
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

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                visit_code='2000',
                subject_identifier=dummy_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

    def year_3_age(self, year_3_years, year_3_months):
        """Returns the age at year 3.
        """
        app_config = django_apps.get_app_config('flourish_caregiver')
        start_date_year_3 = app_config.start_date_year_3

        child_dob = start_date_year_3 - relativedelta(years=year_3_years,
                                                      months=year_3_months)
        return child_dob

    @tag('creff1')
    def test_phq9_referral_required(self):

        visit = ChildVisit.objects.get(visit_code='2000')
        mommy.make_recipe('flourish_child.childphqdeprscreening',
                          child_visit=visit)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.childphqreferral',
                subject_identifier=visit.subject_identifier,
                visit_code='2000').entry_status, REQUIRED)

    def test_phq9_referral_fu_required(self):

        visit = ChildVisit.objects.get(visit_code='2000')
        mommy.make_recipe('flourish_child.childphqdeprscreening',
                          maternal_visit=visit)

        mommy.make_recipe('flourish_child.childphqreferral',
                          maternal_visit=visit,
                          referred_to='receiving_emotional_care')

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.childphqreferralfu',
                subject_identifier=visit.subject_identifier,
                visit_code='2000').entry_status, REQUIRED)

    def test_phq9_post_referral_required(self):

        visit = ChildVisit.objects.get(visit_code='2000')
        mommy.make_recipe('flourish_child.childphqdeprscreening',
                          maternal_visit=visit)

        mommy.make_recipe('flourish_child.childphqreferral',
                          maternal_visit=visit,
                          referred_to='psychiatrist')

        quart_visit = mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                visit_code='2001',
                subject_identifier=visit.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.childphqpostreferral',
                subject_identifier=quart_visit.subject_identifier,
                visit_code='2001').entry_status, REQUIRED)
