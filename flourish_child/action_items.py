from edc_action_item import Action, site_action_items, HIGH_PRIORITY

from flourish_prn.action_items import ChildOffStudyAction

CHILDCONTINUEDCONSENT_STUDY_ACTION = 'submit-childcontinuedconsent-study'

CHILDASSENT_ACTION = 'submit-childassent'

TB_ADOL_STUDY_ACTION = 'submit-tb-adol-off-study'


class ChildContinuedConsentAction(Action):
    name = CHILDCONTINUEDCONSENT_STUDY_ACTION
    display_name = 'Submit Child Continued Consent'
    reference_model = 'flourish_child.childcontinuedconsent'
    admin_site_name = 'flourish_child_admin'
    priority = HIGH_PRIORITY
    singleton = True


class ChildAssentAction(Action):
    name = CHILDASSENT_ACTION
    display_name = 'Submit Child Assent'
    reference_model = 'flourish_child.childassent'
    admin_site_name = 'flourish_child_admin'
    priority = HIGH_PRIORITY
#     singleton = True

class TbAdolOffStudyAction(Action):
    name = TB_ADOL_STUDY_ACTION
    display_name = 'Submit Tb Adol Offstudy'
    reference_model = 'flourish_child.tbadoloffstudy'
    admin_site_name = 'flourish_child_admin'
    priority = HIGH_PRIORITY
    singleton = True

    def get_next_actions(self):
        self.delete_if_new(ChildOffStudyAction)
        return []



site_action_items.register(ChildContinuedConsentAction)
site_action_items.register(ChildAssentAction)
site_action_items.register(TbAdolOffStudyAction)