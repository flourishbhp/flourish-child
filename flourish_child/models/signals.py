from django.apps import apps as django_apps
from django.db.models.signals import post_save
from django.dispatch import receiver
from edc_base.utils import age, get_utcnow
from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from .child_dummy_consent import ChildDummySubjectConsent
from .child_assent import ChildAssent


class CaregiverConsentError(Exception):
    pass


@receiver(post_save, weak=False, sender=ChildAssent,
          dispatch_uid='child_assent_on_post_save')
def child_assent_on_post_save(sender, instance, raw, created, **kwargs):
    """Put subject on cohort a schedule after consenting.
    """
    age = age(instance.dob, get_utcnow()).years
    if not raw and age >= 7:
        caregiver_child_consent_cls = django_apps.get_model('flourish_caregiver.caregiverchildconsent')
        try:
            caregiver_child_consent_obj = caregiver_child_consent_cls.objects.get(subject_identifier=instance.subject_identifier[:-3],
                                              version=instance.version)
        except caregiver_child_consent_cls.DoesNotExist:
            raise CaregiverConsentError('Associated caregiver consent for child for this participant '
                                        'not found')
        else:
            caregiver_child_consent_obj.save(update_fields=['modified', 'user_modified'])


@receiver(post_save, weak=False, sender=ChildDummySubjectConsent,
          dispatch_uid='child_consent_on_post_save')
def child_consent_on_post_save(sender, instance, raw, created, **kwargs):
    """Put subject on cohort a schedule after consenting.
    """
    child_age = age(instance.dob, get_utcnow()).years
    if not raw and child_age < 7:
        caregiver_child_consent_cls = django_apps.get_model('flourish_caregiver.caregiverchildconsent')
        try:
            caregiver_child_consent_obj = caregiver_child_consent_cls.objects.get(subject_identifier=instance.subject_identifier[:-3],
                                              version=instance.version)
        except caregiver_child_consent_cls.DoesNotExist:
            raise CaregiverConsentError('Associated caregiver consent for this participant '
                                        'not found')
        else:
            instance.registration_update_or_create()
            put_on_schedule(caregiver_child_consent_obj.cohort, instance=instance)


def put_on_schedule(cohort, instance=None, subject_identifier=None):
    if instance:
        subject_identifier = subject_identifier or instance.subject_identifier

        cohort_label_lower = ''.join(cohort.split('_'))
        onschedule_model = 'flourish_child.onschedulechild' + cohort_label_lower

        _, schedule = site_visit_schedules.get_by_onschedule_model(
            onschedule_model)

        onschedule_model_cls = django_apps.get_model(onschedule_model)

        schedule_name = cohort + '_schedule_1'

        try:
            onschedule_model_cls.objects.get(
                subject_identifier=instance.subject_identifier,
                schedule_name=schedule_name)
        except onschedule_model_cls.DoesNotExist:
            schedule.put_on_schedule(
                subject_identifier=instance.subject_identifier,
                onschedule_datetime=instance.created,
                schedule_name=schedule_name)
        else:
            schedule.refresh_schedule(
                subject_identifier=instance.subject_identifier)
