from edc_constants.constants import NO


class AssentEligibility:

    def __init__(self, remain_in_study=None, hiv_testing=None,
                 preg_testing=None, child_age=None):
        self.error_message = []
        self.remain_in_study = remain_in_study
        self.hiv_testing = hiv_testing
        self.preg_testing = preg_testing
        self.child_age = child_age

        if self.child_age >= 13 and self.remain_in_study == NO:
            self.error_message.append(
                'Participant is not willing to continue study when they reach 18.')
        if self.hiv_testing == NO:
            self.error_message.append(
                'Participant is not willing to be tested for HIV.')
        if self.preg_testing == NO:
            self.error_message.append(
                'Participant is not will to undergo pregnancy testing.')
        self.is_eligible = False if self.error_message else True


class TbAdolAssentEligibility:
    def __init__(self, *args, **kwargs):
        self.error_message = []

        self.child_age = kwargs['child_age']
        self.citizen = kwargs['citizen']
        self.tb_testing = kwargs['tb_testing']
        self.consent_reviewed = kwargs['consent_reviewed']
        self.study_questions = kwargs['study_questions']
        self.assessment_score = kwargs['assessment_score']
        self.consent_signature = kwargs['consent_signature']

        if self.child_age < 10 or self.child_age > 17:
            self.error_message.append(f'Participint is {self.child_age} old')

        if self.citizen == NO:
            self.error_message.append('The paticipant is not a citizen')

        if self.tb_testing == NO:
            self.error_message.append('The paticipant is not willing to be tested for TB')

        if self.consent_reviewed == NO:
            self.error_message.append('Did not review the consent with participant')

        if self.study_questions == NO:
            self.error_message.append('Did not answer all participant questions about the study')

        if self.assessment_score == NO:
            self.error_message.append('The participant did not understand demostrate some understanding'
                                      ' about the study')
        if self.consent_signature == NO:
            self.error_message.append('The participant did not sign the consent')

        self.is_eligible = False if self.error_message else True


class ContinuedConsentEligibility:

    def __init__(self, remain_in_study=None, hiv_testing=None, preg_testing=None):
        self.error_message = []
        self.remain_in_study = remain_in_study
        self.hiv_testing = hiv_testing
        self.preg_testing = preg_testing
        if self.remain_in_study == NO:
            self.error_message.append(
                'Participant is not willing to continue to participate in the '
                'FLOURISH study')
        if self.hiv_testing == NO:
            self.error_message.append(
                'Participant is not willing to be tested for HIV.')
        if self.preg_testing == NO:
            self.error_message.append(
                'Participant is not will to undergo pregnancy testing.')
        self.is_eligible = False if self.error_message else True
