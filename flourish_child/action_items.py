from edc_action_item import Action, site_action_items, HIGH_PRIORITY

CHILDASSENT_ACTION = 'submit-childassent'

YOUNG_ADULT_LOCATOR_ACTION = 'submit-child-locator'


class ChildAssentAction(Action):
    name = CHILDASSENT_ACTION
    display_name = 'Submit Child Assent'
    reference_model = 'flourish_child.childassent'
    admin_site_name = 'flourish_child_admin'
    priority = HIGH_PRIORITY


class YoungAdultLocatorAction(Action):
    name = YOUNG_ADULT_LOCATOR_ACTION
    display_name = 'Submit Locator'
    reference_model = 'flourish_child.youngadultlocator'
    admin_site_name = 'flourish_child_admin'
    priority = HIGH_PRIORITY


site_action_items.register(ChildAssentAction)
site_action_items.register(YoungAdultLocatorAction)
