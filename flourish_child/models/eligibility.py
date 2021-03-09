from edc_constants.constants import NO


class AssentEligibility:

    def __init__(self, remain_in_study=None, hiv_testing=None, preg_testing=None):
        self.error_message = []
        self.remain_in_study = remain_in_study
        self.hiv_testing = hiv_testing
        self.preg_testing = preg_testing
        if self.remain_in_study == NO:
            self.error_message.append(
                'Participant is not willing to continue study when they reach 18.')
        if self.hiv_testing == NO:
            self.error_message.append(
                'Participant is not willing to be tested for HIV.')
        if self.preg_testing == NO:
            self.error_message.append(
                'Participant is not will to undergo pregnancy testing.')
        self.is_eligible = False if self.error_message else True
