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
    age_in_years = age(instance.dob, get_utcnow()).years
    if not raw and instance.is_eligible:
        if age_in_years >= 7:
            caregiver_child_consent_cls = django_apps.get_model(
                'flourish_caregiver.caregiverchildconsent')
            try:
                caregiver_child_consent_obj = caregiver_child_consent_cls.objects.get(
                    identity=instance.identity,
                    subject_consent__version=instance.version)
            except caregiver_child_consent_cls.DoesNotExist:
                raise CaregiverConsentError('Associated caregiver consent on behalf of child '
                                            'for this participant not found')
            else:
                if caregiver_child_consent_obj.is_eligible:
                    try:
                        dummy_consent_obj = ChildDummySubjectConsent.objects.get(
                            subject_identifier=instance.subject_identifier)
                    except ChildDummySubjectConsent.DoesNotExist:
                        ChildDummySubjectConsent.objects.create(
                                    subject_identifier=instance.subject_identifier,
                                    consent_datetime=instance.consent_datetime,
                                    identity=instance.identity,
                                    cohort=caregiver_child_consent_obj.cohort,
                                    version=instance.version)
                    else:
                        if not dummy_consent_obj.cohort:
                            dummy_consent_obj.cohort = caregiver_child_consent_obj.cohort
                            dummy_consent_obj.save()

                    caregiver_child_consent_obj.subject_identifier = instance.subject_identifier
                    caregiver_child_consent_obj.save(update_fields=['subject_identifier',
                                                                    'modified', 'user_modified'])


@receiver(post_save, weak=False, sender=ChildDummySubjectConsent,
          dispatch_uid='child_consent_on_post_save')
def child_consent_on_post_save(sender, instance, raw, created, **kwargs):
    """Put subject on cohort a schedule after consenting.
    """
    if instance.cohort:
        put_on_schedule(instance.cohort, instance=instance)


def put_on_schedule(cohort, instance=None, subject_identifier=None):
    if instance:
        instance.registration_update_or_create()
        subject_identifier = subject_identifier or instance.subject_identifier

        cohort_label_lower = ''.join(cohort.split('_'))
        onschedule_model = 'flourish_child.onschedulechild' + cohort_label_lower

        _, schedule = site_visit_schedules.get_by_onschedule_model(
            onschedule_model)

        onschedule_model_cls = django_apps.get_model(onschedule_model)

        if 'pool' not in cohort:
            schedule_name = 'child_' + cohort[-1:] + '_schedule1'
        else:
            schedule_name = 'child_pool_schedule1'

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
