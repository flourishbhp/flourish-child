
from .model_mixins.child_socio_demographic_mixin import ChildSocioDemographicMixin


from .child_crf_model_mixin import ChildCrfModelMixin


class ChildSocioDemographic(ChildSocioDemographicMixin, ChildCrfModelMixin):

    """ A model completed by the user on Demographics form for all infants.
    """
    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = "Child Sociodemographic Data"
        verbose_name_plural = "Child Sociodemographic Data"
