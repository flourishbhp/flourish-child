from edc_base.model_mixins import ListModelMixin, BaseUuidModel


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


class SolidFoods(ListModelMixin, BaseUuidModel):
    pass
