
from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_mixins import ListModelMixin as BaseListModelMixin


class ListModelMixin(BaseListModelMixin):
    name = models.CharField(
        verbose_name='Name',
        max_length=250,
        db_index=True,
        help_text='(suggest 40 characters max.)',
    )

    class Meta:
        abstract = True


class ChronicConditions(ListModelMixin, BaseUuidModel):
    pass


class ChildMedications(ListModelMixin, BaseUuidModel):
    pass


class WcsDxAdult(ListModelMixin, BaseUuidModel):
    pass


class ChildDiseases(ListModelMixin, BaseUuidModel):
    pass


class ChildCovidSymptoms(ListModelMixin, BaseUuidModel):
    pass


class ChildCovidSymptomsAfter14Days(ListModelMixin, BaseUuidModel):
    pass


class EmoSupportType(ListModelMixin, BaseUuidModel):
    pass


class EmoHealthImproved(ListModelMixin, BaseUuidModel):
    pass


class SolidFoods(ListModelMixin, BaseUuidModel):
    pass


class TbKnowledgeMedium(ListModelMixin, BaseUuidModel):
    pass


class HIVKnowledgeMedium(ListModelMixin, BaseUuidModel):
    pass


class HealthCareCenter(ListModelMixin, BaseUuidModel):
    pass


class TbRoutineScreenAdolMedium(ListModelMixin, BaseUuidModel):
    pass


class StaffMember(ListModelMixin, BaseUuidModel):
    pass


class TbDiagnostics(ListModelMixin, BaseUuidModel):
    pass


class OutpatientSymptoms(ListModelMixin, BaseUuidModel):
    pass


class Medications(ListModelMixin, BaseUuidModel):
    pass


class GeneralSymptoms(ListModelMixin, BaseUuidModel):
    pass


class OutpatientMedications(ListModelMixin, BaseUuidModel):
    pass


class ChildSocialWorkReferralList(ListModelMixin, BaseUuidModel):
    pass


class ChildTBTests(ListModelMixin, BaseUuidModel):
    pass


class ChildHIVTestVisits(ListModelMixin, BaseUuidModel):
    pass


class ChildHIVNotTestedReason(ListModelMixin, BaseUuidModel):
    pass


class ChildTbReferralReasons(ListModelMixin, BaseUuidModel):
    pass
