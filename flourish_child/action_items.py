from edc_action_item import Action, site_action_items, HIGH_PRIORITY

from flourish_prn.action_items import ChildOffStudyAction

CHILDCONTINUEDCONSENT_STUDY_ACTION = 'submit-childcontinuedconsent-study'

CHILDASSENT_ACTION = 'submit-childassent'

YOUNG_ADULT_LOCATOR_ACTION = 'submit-child-locator'


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


class YoungAdultLocatorAction(Action):
    name = YOUNG_ADULT_LOCATOR_ACTION
    display_name = 'Submit Locator'
    reference_model = 'flourish_child.YoungAdultLocator'
    admin_site_name = 'flourish_child_admin'
    priority = HIGH_PRIORITY
    singleton = True


site_action_items.register(ChildContinuedConsentAction)
site_action_items.register(ChildAssentAction)
site_action_items.register(YoungAdultLocatorAction)
