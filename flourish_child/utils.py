from django.utils import timezone

from flourish_caregiver.helper_classes.cohort import Cohort
from flourish_child.models import ChildDataset


def over_age_limit(self):
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
