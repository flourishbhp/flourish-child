from django.db import models
from edc_base.model_mixins.base_uuid_model import BaseUuidModel
from edc_constants.choices import YES_NO

from ..choices import INFANT_VACCINATIONS, FEEDING_CHOICES, BF_ESTIMATED
from .child_crf_model_mixin import ChildCrfModelMixin


class BirthFeedingVaccine(ChildCrfModelMixin):
    """ A model completed by the user on the infant's feeding &
    vaccination/ immunization. """

    feeding_after_delivery = models.CharField(
        max_length=50,
        choices=FEEDING_CHOICES,
        verbose_name="How was the infant being fed immediately after delivery? ",
        help_text=" ...before discharge from maternity")

    breastfeed_start_dt = models.DateField(
        verbose_name='When did you begin breastfeeding your infant?',
        null=True,
        blank=True)

    breastfeed_start_est = models.CharField(
        verbose_name='Is this date estimated?',
        choices=BF_ESTIMATED,
        null=True,
        blank=True,
        max_length=15, )

    formulafeed_start_dt = models.DateField(
        verbose_name='When did you begin feeding your infant formula?',
        null=True,
        blank=True)

    formulafeed_start_est = models.CharField(
        verbose_name='Is this date estimated?',
        choices=YES_NO,
        null=True,
        blank=True,
        max_length=3, )

    comments = models.TextField(
        max_length=250,
        verbose_name="Comment if any additional pertinent information: ",
        blank=True,
        null=True)

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = "Birth Feeding & Vaccination"


class BirthVaccines(BaseUuidModel):

    birth_feed_vaccine = models.ForeignKey(
        BirthFeedingVaccine, on_delete=models.CASCADE)

    vaccination = models.CharField(
        choices=INFANT_VACCINATIONS,
        verbose_name="Since delivery, did the child receive any of the following vaccinations",
        max_length=100)

    vaccine_date = models.DateField(
        verbose_name='Date Vaccine was given')

    class Meta:
        app_label = 'flourish_child'
        verbose_name = "Birth Vaccines"
        verbose_name_plural = "Birth Vaccines"
        unique_together = ('birth_feed_vaccine', 'vaccination', 'vaccine_date')
