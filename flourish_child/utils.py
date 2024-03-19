import logging

from celery.app import shared_task
from celery.signals import worker_process_init
from django.utils import timezone

from flourish_caregiver.helper_classes.cohort import Cohort
from flourish_child.models import ChildDataset

logger = logging.getLogger(__name__)


@worker_process_init.connect
def configure_workers(sender=None, conf=None, **kwargs):
    from Crypto import Random
    Random.atfork()


@shared_task
def over_age_limit():
    """Sets age today on a child dataset.
    """
    child_data = ChildDataset.objects.all()
    over_age_limit = []
    for child in child_data:
        age = Cohort().age_at_enrollment(
            child_dob=child.dob, check_date=timezone.now().date())
        child.age_today = age
        child.age_calculation_date = timezone.now().date()
        child.save()
