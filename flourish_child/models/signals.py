from django.apps import apps as django_apps
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from edc_action_item.site_action_items import site_action_items
from edc_base.utils import age, get_utcnow
from edc_constants.constants import OPEN, NEW, POS
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from flourish_prn.action_items import CHILDOFF_STUDY_ACTION
from flourish_prn.models import ChildOffStudy
from .child_dummy_consent import ChildDummySubjectConsent
from .child_assent import ChildAssent
from .child_hiv_rapid_test_counseling import ChildHIVRapidTestCounseling
from .child_preg_testing import ChildPregTesting
from .child_continued_consent import ChildContinuedConsent


class CaregiverConsentError(Exception):
    pass


@receiver(post_save, weak=False, sender=ChildAssent,
          dispatch_uid='child_assent_on_post_save')
def child_assent_on_post_save(sender, instance, raw, created, **kwargs):
    """Put subject on schedule after consenting.
    """
    age_in_years = age(instance.dob, get_utcnow()).years
    if not raw and instance.is_eligible:

        if age_in_years >= 7:
            caregiver_prev_enrolled_cls = django_apps.get_model(
                    'flourish_caregiver.caregiverpreviouslyenrolled')
            try:
                caregiver_prev_enrolled_cls.objects.get(
                    subject_identifier=instance.subject_identifier[:-3])
            except caregiver_prev_enrolled_cls.DoesNotExist:
                pass
            else:
                caregiver_child_consent_cls = django_apps.get_model(
                    'flourish_caregiver.caregiverchildconsent')
                try:
                    caregiver_child_consent_obj = caregiver_child_consent_cls.objects.get(
                        subject_identifier=instance.subject_identifier,
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
                                        dob=instance.dob,
                                        cohort=caregiver_child_consent_obj.cohort,
                                        version=instance.version)
                        else:
                            if not dummy_consent_obj.cohort:
                                dummy_consent_obj.cohort = caregiver_child_consent_obj.cohort
                                dummy_consent_obj.save()

                        caregiver_child_consent_obj.subject_identifier = instance.subject_identifier
                        caregiver_child_consent_obj.save(
                            update_fields=['subject_identifier', 'modified', 'user_modified'])


@receiver(post_save, weak=False, sender=ChildDummySubjectConsent,
          dispatch_uid='child_consent_on_post_save')
def child_consent_on_post_save(sender, instance, raw, created, **kwargs):
    """Put subject on cohort a schedule after consenting.
    """
    if instance.cohort:
        maternal_delivery_cls = django_apps.get_model('flourish_caregiver.maternaldelivery')
        try:
            maternal_delivery_cls.objects.get(
                delivery_datetime=instance.consent_datetime,
                subject_identifier=instance.subject_identifier[:-3])
        except maternal_delivery_cls.DoesNotExist:
            pass
        else:
            put_on_schedule((instance.cohort + '_birth'), instance=instance)

        put_cohort_onschedule(instance.cohort, instance=instance)


@receiver(post_save, weak=False, sender=ChildHIVRapidTestCounseling,
          dispatch_uid='child_rapid_test_on_post_save')
def child_rapid_test_on_post_save(sender, instance, raw, created, **kwargs):
    """Take the participant offstudy if HIV result is positive.
    """
    trigger_action_item(instance, 'result', POS,
                        ChildOffStudy, CHILDOFF_STUDY_ACTION,
                        instance.child_visit.appointment.subject_identifier,
                        repeat=True)


@receiver(post_save, weak=False, sender=ChildPregTesting,
          dispatch_uid='child_preg_testing_on_post_save')
def child_preg_testing_on_post_save(sender, instance, raw, created, **kwargs):
    """Take the participant offstudy if pregnancy test result is positive.
    """
    trigger_action_item(instance, 'preg_test_result', POS,
                        ChildOffStudy, CHILDOFF_STUDY_ACTION,
                        instance.child_visit.appointment.subject_identifier,
                        repeat=True)


@receiver(post_save, weak=False, sender=ChildContinuedConsent,
          dispatch_uid='child_continued_consent_on_post_save')
def child_continued_consent_on_post_save(sender, instance, raw, created, **kwargs):
    """Take the participant offstudy if child ineligible on continued consent.
    """
    trigger_action_item(instance, 'is_eligible', False,
                        ChildOffStudy, CHILDOFF_STUDY_ACTION,
                        instance.subject_identifier,
                        repeat=True)


def put_cohort_onschedule(cohort, instance):

    if cohort is not None and 'sec' in cohort or 'pool' in cohort:
        put_on_schedule(cohort, instance=instance)
    else:
        put_on_schedule(cohort + '_enrol', instance=instance)
        put_on_schedule(cohort + '_quart', instance=instance)
        # put_on_schedule(cohort + '_fu', instance=instance,
                        # base_appt_datetime=django_apps.get_app_config(
                            # 'edc_protocol').study_open_datetime)


def put_on_schedule(cohort, instance=None, subject_identifier=None,
                    base_appt_datetime=None):

    if instance:
        instance.registration_update_or_create()
        subject_identifier = subject_identifier or instance.subject_identifier

        cohort_label_lower = ''.join(cohort.split('_'))

        if 'enrol' in cohort:
            cohort_label_lower = cohort_label_lower.replace('enrol', 'enrollment')
        elif 'quart' in cohort:
            cohort_label_lower = cohort_label_lower.replace('quart', 'quarterly')

        onschedule_model = 'flourish_child.onschedulechild' + cohort_label_lower

        onschedule_model_cls = django_apps.get_model(onschedule_model)

        if 'pool' not in cohort:
            schedule_name = cohort.replace('cohort', 'child') + '_schedule1'
        else:
            schedule_name = 'child_pool_schedule1'

        _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            onschedule_model=onschedule_model, name=schedule_name)

        try:
            onschedule_model_cls.objects.get(
                subject_identifier=subject_identifier,
                schedule_name=schedule_name)
        except onschedule_model_cls.DoesNotExist:
            schedule.put_on_schedule(
                subject_identifier=subject_identifier,
                onschedule_datetime=base_appt_datetime,
                schedule_name=schedule_name,
                base_appt_datetime=base_appt_datetime)
        else:
            schedule.refresh_schedule(
                subject_identifier=subject_identifier)


def trigger_action_item(obj, field, response, model_cls,
                        action_name, subject_identifier,
                        repeat=False):

    action_cls = site_action_items.get(
        model_cls.action_name)
    action_item_model_cls = action_cls.action_item_model_cls()

    if getattr(obj, field) == response:
        try:
            model_cls.objects.get(subject_identifier=subject_identifier)
        except model_cls.DoesNotExist:
            trigger = True
        else:
            trigger = repeat
        if trigger:
            try:
                action_item_obj = action_item_model_cls.objects.get(
                    subject_identifier=subject_identifier,
                    action_type__name=action_name)
            except action_item_model_cls.DoesNotExist:
                action_cls = site_action_items.get(action_name)
                action_cls(subject_identifier=subject_identifier)
            else:
                action_item_obj.status = OPEN
                action_item_obj.save()
    else:
        try:
            action_item = action_item_model_cls.objects.get(
                Q(status=NEW) | Q(status=OPEN),
                subject_identifier=subject_identifier,
                action_type__name=action_name)
        except action_item_model_cls.DoesNotExist:
            pass
        else:
            action_item.delete()
