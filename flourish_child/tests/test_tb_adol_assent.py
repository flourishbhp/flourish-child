import datetime
from django.test import tag, SimpleTestCase as TestCase
from edc_constants.constants import NO, YES
from ..models.eligibility import TbAdolAssentEligibility


@tag('tbadol')
class TestTbAdolAssentEligibility(TestCase):
    
    def setUp(self):
        self.data = {
             'child_age': 15,
             'citizen' : YES,
             'tb_testing': YES,
             'consent_reviewed': YES,
             'study_questions': YES,
             'assessment_score': YES,
             'consent_signature': YES
        }
        

        
        
    def test_citizen_required(self):
        self.data['citizen'] = NO
        elibility = TbAdolAssentEligibility(**self.data)
        
        self.assertFalse(elibility.is_eligible)
        self.assertTrue(elibility.error_message)
        
    def test_age_is_withing_10_and_17(self):
        self.data['child_age'] = 15
        elibility = TbAdolAssentEligibility(**self.data)
        
        self.assertTrue(elibility.is_eligible)
        self.assertFalse(elibility.error_message)
        
        self.data['child_age'] = 9
        elibility = TbAdolAssentEligibility(**self.data)
        
        self.assertFalse(elibility.is_eligible)
        self.assertTrue(elibility.error_message)
        
    def test_tb_testing_required(self):
        self.data['tb_testing'] = NO
        elibility = TbAdolAssentEligibility(**self.data)
        
        self.assertFalse(elibility.is_eligible)
        self.assertTrue(elibility.error_message)
        
        
    def test_consent_reviewed_required(self):
        
        self.data['consent_reviewed'] = NO
        elibility = TbAdolAssentEligibility(**self.data)
        
        self.assertFalse(elibility.is_eligible)
        self.assertTrue(elibility.error_message)
        
    def test_study_questions_required(self):
        
        self.data['study_questions'] = NO
        elibility = TbAdolAssentEligibility(**self.data)
        
        self.assertFalse(elibility.is_eligible)
        self.assertTrue(elibility.error_message)
        
    def test_assessment_score_required(self):
        
        self.data['assessment_score'] = NO
        elibility = TbAdolAssentEligibility(**self.data)
        
        self.assertFalse(elibility.is_eligible)
        self.assertTrue(elibility.error_message)
    
    def test_consent_signature_required(self):
        
        self.data['consent_signature'] = NO
        elibility = TbAdolAssentEligibility(**self.data)
        
        self.assertFalse(elibility.is_eligible)
        self.assertTrue(elibility.error_message)
        
        