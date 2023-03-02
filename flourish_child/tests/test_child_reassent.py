from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_base import get_utcnow
from edc_constants.constants import NOT_APPLICABLE
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy

from ..models import ChildDummySubjectConsent


@tag('reassent')
class TestChildReassent(TestCase):

    def setUp(self):
        import_holidays()

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '2'}

        maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=10, months=2),
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-infected',
            'study_maternal_identifier': '12345',
            'protocol': 'Mashi',
            'preg_pi': 1}

        self.child_dataset_options = {
            'infant_hiv_exposed': 'Unexposed',
            'infant_enrolldate': get_utcnow(),
            'study_maternal_identifier': '12345',
            'study_child_identifier': '1234'}

        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=10, months=2),
            **self.child_dataset_options)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            **maternal_dataset_options)

        self.flourish_consent_version = mommy.make_recipe(
            'flourish_caregiver.flourishconsentversion',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            version='2',
            child_version='2')

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,)

        self.subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=NOT_APPLICABLE,
            **self.options)

        caregiver_child_consent_obj = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=self.subject_consent,
            study_child_identifier=self.child_dataset_options.get('study_child_identifier'),
            identity='126513789',
            confirm_identity='126513789',
            child_dob=(get_utcnow() - relativedelta(years=10, months=2)).date(),)
        caregiver_child_consent_obj.version = '2'
        caregiver_child_consent_obj.save()

        self.child_subject_identifier = caregiver_child_consent_obj.subject_identifier

        mommy.make_recipe(
                'flourish_caregiver.caregiverpreviouslyenrolled',
                subject_identifier=self.subject_consent.subject_identifier)

        mommy.make_recipe(
            'flourish_child.childassent',
            subject_identifier=caregiver_child_consent_obj.subject_identifier,
            dob=(get_utcnow() - relativedelta(years=10, months=2)).date(),
            identity=caregiver_child_consent_obj.identity,
            confirm_identity=caregiver_child_consent_obj.identity,
            version=self.subject_consent.version)

    def test_reassent_v3(self):
        self.assertEqual(ChildDummySubjectConsent.objects.filter(
            subject_identifier=self.child_subject_identifier).count(), 1)

        self.flourish_consent_version.version = '3'
        self.flourish_consent_version.child_version = '3'
        self.flourish_consent_version.save()

        self.options.update(version='3')

        consent_v3 = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            subject_identifier=self.subject_consent.subject_identifier,
            screening_identifier=self.subject_consent.screening_identifier,
            breastfeed_intent=NOT_APPLICABLE,
            **self.options)

        child_consent_v3 = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_identifier=self.child_subject_identifier,
            subject_consent=consent_v3,
            study_child_identifier=self.child_dataset_options.get('study_child_identifier'),
            identity='126513789',
            confirm_identity='126513789',
            child_dob=(get_utcnow() - relativedelta(years=10, months=2)).date(),
            version='3')

        mommy.make_recipe(
            'flourish_child.childassent',
            subject_identifier=child_consent_v3.subject_identifier,
            screening_identifier=consent_v3.screening_identifier,
            dob=(get_utcnow() - relativedelta(years=10, months=2)).date(),
            identity=child_consent_v3.identity,
            confirm_identity=child_consent_v3.identity,
            version=child_consent_v3.version)

        self.assertEqual(ChildDummySubjectConsent.objects.filter(
            subject_identifier=self.child_subject_identifier).count(), 2)

        self.assertEqual(ChildDummySubjectConsent.objects.filter(
            subject_identifier=self.child_subject_identifier).latest(
                'consent_datetime').version, '3')
