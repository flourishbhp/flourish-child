from django.db import models
from django.db.models.deletion import PROTECT
from edc_base.model_mixins import BaseUuidModel, FormAsJSONModelMixin
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_metadata.model_mixins.updates import UpdatesCrfMetadataModelMixin
from edc_model_admin import ModelAdminFormInstructionsMixin
from edc_reference.model_mixins import ReferenceModelMixin
from edc_visit_tracking.model_mixins import CrfModelMixin as BaseCrfModelMixin
from edc_visit_tracking.model_mixins import PreviousVisitModelMixin

from edc_consent.model_mixins import RequiresConsentFieldsModelMixin
from edc_visit_schedule.model_mixins import SubjectScheduleCrfModelMixin

from .child_visit import ChildVisit


class ChildCrfModelMixin(
        BaseCrfModelMixin, SubjectScheduleCrfModelMixin,
        RequiresConsentFieldsModelMixin, PreviousVisitModelMixin,
        UpdatesCrfMetadataModelMixin, SiteModelMixin,
        ModelAdminFormInstructionsMixin, FormAsJSONModelMixin,
        ReferenceModelMixin, BaseUuidModel):

    """ Base model for all scheduled models
    """

    offschedule_compare_dates_as_datetimes = False
    child_visit = models.OneToOneField(ChildVisit, on_delete=PROTECT)

    def natural_key(self):
        return self.child_visit.natural_key()

    natural_key.dependencies = [
        'flourish_child.childvisit',
        'sites.Site',
        'edc_appointment.appointment']

    class Meta:
        abstract = True
