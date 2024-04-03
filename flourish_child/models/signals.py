from datetime import datetime

import pytz
from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import model_to_dict, ValidationError
from edc_appointment.constants import COMPLETE_APPT
from edc_base.utils import age, get_utcnow
from edc_constants.constants import IND, MALE, NEG, NO, UNKNOWN, YES
from edc_data_manager.models import DataActionItem
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from edc_visit_tracking.constants import MISSED_VISIT
from edc_visit_schedule.subject_schedule import InvalidOffscheduleDate
from flourish_child.models.adol_hiv_testing import HivTestingAdol
from flourish_child.models.adol_tb_lab_results import TbLabResultsAdol
from flourish_child.models.adol_tb_presence_household_member import \
    TbPresenceHouseholdMembersAdol
from flourish_child.models.adol_tb_referral import TbReferalAdol
from flourish_child.models.child_appointment import Appointment as ChildAppointment
from flourish_child.models.child_birth import ChildBirth
from flourish_child.models.tb_adol_assent import TbAdolAssent
from flourish_child.models.tb_visit_screen_adol import TbVisitScreeningAdolescent
from flourish_prn.action_items import CHILD_DEATH_REPORT_ACTION, \
    MISSED_BIRTH_VISIT_ACTION, TB_ADOL_STUDY_ACTION
from flourish_prn.models import TBAdolOffStudy
from flourish_prn.models.child_death_report import ChildDeathReport
from pre_flourish.helper_classes import MatchHelper
from .child_assent import ChildAssent
from .child_clinician_notes import ClinicianNotesImage
from .child_dummy_consent import ChildDummySubjectConsent
from .child_visit import ChildVisit
from ..action_items import YOUNG_ADULT_LOCATOR_ACTION
from ..helper_classes import ChildFollowUpBookingHelper, ChildOnScheduleHelper
from ..helper_classes.utils import (child_utils, notification, stamp_image,
                                    trigger_action_item)
from ..models import AcademicPerformance, ChildOffSchedule, ChildSocioDemographic
from ..models import ChildPreHospitalizationInline
from ..models.child_clinical_measurements import ChildClinicalMeasurements
from ..models.child_continued_consent import ChildContinuedConsent
from ..models.young_adult_locator import YoungAdultLocator


class CaregiverConsentError(Exception):
    pass


@receiver(post_save, weak=False, sender=ChildSocioDemographic,
          dispatch_uid='child_socio_demographic_post_save')
def child_socio_demographic_post_save(sender, instance, raw, created, **kwargs):
    """
    Update academic perfomance in the same visit without affecting any other forms
    beyond and after that particular visit
    """

    child_visit_id = instance.child_visit.id

    try:

        academic_perfomance = AcademicPerformance.objects.get(
            child_visit_id=child_visit_id)

    except AcademicPerformance.DoesNotExist:
        pass

    else:
        # update only if the academic perfomance education level are different
        if academic_perfomance.education_level != instance.education_level:
            academic_perfomance.education_level = instance.education_level
            academic_perfomance.save()


@receiver(post_save, weak=False, sender=ChildAssent,
          dispatch_uid='child_assent_on_post_save')
def child_assent_on_post_save(sender, instance, raw, created, **kwargs):
    """Put subject on schedule after consenting.
    """
    age_in_years = age(instance.dob, get_utcnow()).years

    if not raw and instance.is_eligible:
        if age_in_years >= 7:
            caregiver_child_consent_cls = django_apps.get_model(
                'flourish_caregiver.caregiverchildconsent')
            try:
                caregiver_child_consent_obj = caregiver_child_consent_cls.objects.get(
                    subject_identifier=instance.subject_identifier,
                    version=instance.version)
            except caregiver_child_consent_cls.DoesNotExist:
                raise CaregiverConsentError('Associated caregiver consent on behalf of '
                                            'child for this participant not found')
            else:
                caregiver_subject_identifier = (
                    caregiver_child_consent_obj.subject_consent.subject_identifier)
                if caregiver_child_consent_obj.is_eligible:
                    try:
                        dummy_consent_obj = ChildDummySubjectConsent.objects.get(
                            subject_identifier=instance.subject_identifier,
                            version=instance.version)
                    except ChildDummySubjectConsent.DoesNotExist:
                        ChildDummySubjectConsent.objects.create(
                            subject_identifier=instance.subject_identifier,
                            consent_datetime=instance.consent_datetime,
                            identity=instance.identity,
                            dob=instance.dob,
                            cohort=caregiver_child_consent_obj.cohort,
                            relative_identifier=caregiver_subject_identifier,
                            version=instance.version)
                    else:
                        caregiver_prev_enrolled_cls = django_apps.get_model(
                            'flourish_caregiver.caregiverpreviouslyenrolled')
                        try:
                            caregiver_prev_enrolled_cls.objects.get(
                                subject_identifier=caregiver_subject_identifier)
                        except caregiver_prev_enrolled_cls.DoesNotExist:
                            pass
                        else:
                            dummy_consent_obj.save()

                        caregiver_child_consent_obj.subject_identifier = \
                            instance.subject_identifier
                        caregiver_child_consent_obj.save(
                            update_fields=['subject_identifier', 'modified',
                                           'user_modified'])


@receiver(post_save, weak=False, sender=ChildAppointment)
def child_appointment_on_post_save(sender, instance, raw, created, **kwargs):
    if ('tb_adol_followup_schedule' == instance.schedule_name and
            instance.appt_status == COMPLETE_APPT):
        trigger_action_item(TBAdolOffStudy, TB_ADOL_STUDY_ACTION,
                            instance.subject_identifier,
                            repeat=True)


@receiver(post_save, weak=False, sender=ChildDummySubjectConsent,
          dispatch_uid='child_consent_on_post_save')
def child_consent_on_post_save(sender, instance, raw, created, **kwargs):
    """Put subject on cohort a schedule after consenting.
    """
    if not raw:

        caregiver_child_consent_cls = django_apps.get_model(
            'flourish_caregiver.caregiverchildconsent')

        caregiver_prev_enrolled_cls = django_apps.get_model(
            'flourish_caregiver.caregiverpreviouslyenrolled')

        maternal_delivery_cls = django_apps.get_model(
            'flourish_caregiver.maternaldelivery')

        child_prev_enrolled = caregiver_child_consent_cls.objects.filter(
            subject_identifier=instance.subject_identifier,
            study_child_identifier__isnull=False).exists()

        helper_cls = ChildOnScheduleHelper(
            subject_identifier=instance.subject_identifier,
            cohort=instance.cohort)

        if child_prev_enrolled:
            # The criteria is for child from a previous study
            try:
                prev_enrolled = caregiver_prev_enrolled_cls.objects.get(
                    subject_identifier=instance.relative_identifier)
            except caregiver_prev_enrolled_cls.DoesNotExist:
                pass
            else:
                helper_cls.base_appt_datetime = prev_enrolled.report_datetime
                helper_cls.put_cohort_onschedule(instance, )

        else:

            try:
                maternal_delivery_obj = maternal_delivery_cls.objects.get(
                    delivery_datetime=instance.consent_datetime,
                    subject_identifier=instance.relative_identifier)
            except maternal_delivery_cls.DoesNotExist:
                pass
            else:
                helper_cls.cohort = (instance.cohort + '_birth')
                helper_cls.base_appt_datetime = maternal_delivery_obj.created
                helper_cls.put_on_schedule(instance, )


@receiver(post_save, weak=False, sender=TbVisitScreeningAdolescent,
          dispatch_uid='adol_tb_visit_presence_on_post_save')
def child_tb_visit_screening_on_post_save(sender, instance, raw, created, **kwargs):
    if (instance.cough_duration == NO or instance.fever_duration == NO or
            instance.night_sweats == NO or instance.weight_loss == NO):
        trigger_action_item(TBAdolOffStudy, TB_ADOL_STUDY_ACTION,
                            instance.child_visit.subject_identifier,
                            repeat=True)


@receiver(post_save, weak=False, sender=TbPresenceHouseholdMembersAdol,
          dispatch_uid='adol_tb_presence_on_post_save')
def child_tb_presence_on_post_save(sender, instance, raw, created, **kwargs):
    if instance.tb_referral == YES:
        trigger_action_item(TBAdolOffStudy, TB_ADOL_STUDY_ACTION,
                            instance.child_visit.subject_identifier,
                            repeat=True)


@receiver(post_save, weak=False, sender=HivTestingAdol,
          dispatch_uid='hiv_testing_on_post_save')
def child_hiv_testing_on_post_save(sender, instance, raw, created, **kwargs):
    if instance.last_result in [NEG, IND,
                                UNKNOWN] or instance.referred_for_treatment == NO:
        trigger_action_item(TBAdolOffStudy, TB_ADOL_STUDY_ACTION,
                            instance.child_visit.subject_identifier,
                            repeat=True)


@receiver(post_save, weak=False, sender=TbLabResultsAdol,
          dispatch_uid='child_tb_lab_results_on_post_save')
def child_tb_lab_results_on_post_save(sender, instance, raw, created, **kwargs):
    if instance.quantiferon_result == NEG:
        trigger_action_item(TBAdolOffStudy, TB_ADOL_STUDY_ACTION,
                            instance.child_visit.subject_identifier,
                            repeat=True)


@receiver(post_save, weak=False, sender=ChildVisit,
          dispatch_uid='child_visit_on_post_save')
def child_visit_on_post_save(sender, instance, raw, created, **kwargs):
    """
    Check is the child visit with visit_code 200OD is missed
    """
    missed_birth_visit_cls = django_apps.get_model(
        'flourish_prn.missedbirthvisit')

    if getattr(instance, 'reason') == MISSED_VISIT and getattr(instance,
                                                               'visit_code') == '2000D':
        trigger_action_item(missed_birth_visit_cls, MISSED_BIRTH_VISIT_ACTION,
                            instance.subject_identifier,
                            repeat=True)

    """
    - Put subject on quarterly schedule at enrollment visit.
    """
    if getattr(instance, 'survival_status') == 'dead':
        trigger_action_item(ChildDeathReport, CHILD_DEATH_REPORT_ACTION,
                            instance.subject_identifier)

    if not raw and created and instance.visit_code in ['2000', '2000D', '3000',
                                                       '3000A', '3000B', '3000C']:

        if 'sec' in instance.schedule_name:

            cohort_list = instance.schedule_name.split('_')

            cohort = '_'.join(['cohort', cohort_list[1], 'sec_qt'])
        elif 'fu' in instance.schedule_name:

            cohort_list = instance.schedule_name.split('_')

            cohort = '_'.join(['cohort', cohort_list[1], 'fu_qt'])
        else:
            cohort_list = instance.schedule_name.split('_')

            cohort = '_'.join(['cohort', cohort_list[1], 'quarterly'])

        helper_cls = ChildOnScheduleHelper(
            subject_identifier=instance.subject_identifier,
            base_appt_datetime=instance.report_datetime.replace(
                microsecond=0),
            cohort=cohort)
        helper_cls.put_on_schedule(instance, )


@receiver(post_save, weak=False, sender=TbAdolAssent,
          dispatch_uid='tb_adol_on_post_save')
def tb_adol_assent_on_post_save(sender, instance, raw, created, **kwargs):
    if instance.is_eligible:
        helper_cls = ChildOnScheduleHelper(
            subject_identifier=instance.subject_identifier,
            base_appt_datetime=instance.consent_datetime.replace(
                microsecond=0),
            cohort='tb_adol')
        helper_cls.put_on_schedule(instance, )


@receiver(post_save, weak=False, sender=TbReferalAdol,
          dispatch_uid='tb_referral_adol_on_post_save')
def tb_referral_adol_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw:
        onschedule_model = 'flourish_child.onscheduletbadolfollowupschedule'
        schedule_name = 'tb_adol_followup_schedule'
        _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            onschedule_model=onschedule_model, name=schedule_name)
        child_visit = getattr(instance, 'child_visit', None)
        subject_identifier = getattr(child_visit, 'subject_identifier', None)
        referral_dt = getattr(instance, 'referral_date', None)
        tz = pytz.timezone('Africa/Gaborone')
        onschedule_datetime = datetime.combine(
            referral_dt, get_utcnow().time(), tz)

        if not schedule.is_onschedule(subject_identifier=subject_identifier,
                                      report_datetime=onschedule_datetime):
            schedule.put_on_schedule(
                subject_identifier=subject_identifier,
                onschedule_datetime=onschedule_datetime.replace(microsecond=0),
                schedule_name=schedule_name,
                base_appt_datetime=onschedule_datetime.replace(microsecond=0))


@receiver(post_save, weak=False, sender=ChildBirth,
          dispatch_uid='child_visit_on_post_save')
def child_birth_on_post_save(sender, instance, raw, created, **kwargs):
    """
    - Put subject on birth schedule.
    """
    if not raw and created:
        maternal_delivery_cls = django_apps.get_model(
            'flourish_caregiver.maternaldelivery')

        caregiver_subject_identifier = child_utils.caregiver_subject_identifier(
            subject_identifier=instance.subject_identifier)
        base_appt_datetime = None
        try:
            maternal_delivery_obj = maternal_delivery_cls.objects.get(
                subject_identifier=caregiver_subject_identifier,
                child_subject_identifier=instance.subject_identifier)
        except maternal_delivery_cls.DoesNotExist:
            pass
        else:
            if maternal_delivery_obj.live_infants_to_register == 1:
                base_appt_datetime = maternal_delivery_obj.delivery_datetime.replace(
                    microsecond=0)

                helper_cls = ChildOnScheduleHelper(
                    subject_identifier=instance.subject_identifier,
                    base_appt_datetime=base_appt_datetime,
                    cohort='child_cohort_a_birth')
                helper_cls.put_on_schedule(instance, )

        caregiver_child_consent_cls = django_apps.get_model(
            'flourish_caregiver.caregiverchildconsent')

        caregiver_child_consent_objs = caregiver_child_consent_cls.objects.filter(
            subject_identifier=instance.subject_identifier)

        for caregiver_child_consent_obj in caregiver_child_consent_objs:
            caregiver_child_consent_obj.first_name = instance.first_name
            caregiver_child_consent_obj.last_name = instance.last_name
            caregiver_child_consent_obj.gender = instance.gender
            caregiver_child_consent_obj.child_dob = instance.dob
            caregiver_child_consent_obj.save()

        notification(
            subject_identifier=instance.subject_identifier,
            user_created=instance.user_created,
            subject="'Add name and DOB to the paper informed consent form'")

        # book participant for followup
        booking_helper = ChildFollowUpBookingHelper()
        booking_dt = base_appt_datetime + relativedelta(years=1)
        booking_helper.schedule_fu_booking(
            instance.subject_identifier, booking_dt)


@receiver(post_save, weak=False, sender=ClinicianNotesImage,
          dispatch_uid='clinician_notes_image_on_post_save')
def clinician_notes_image_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw and created:
        stamp_image(instance)


@receiver(post_save, weak=False, sender=AcademicPerformance,
          dispatch_uid='academic_performance_on_post_save')
def academic_performance_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw and created:
        overall_performance = getattr(instance, 'overall_performance', None)
        if overall_performance and overall_performance == 'pending':
            child_visit = instance.child_visit
            subject = f'Pending academic results at visit {child_visit.visit_code}'
            try:
                DataActionItem.objects.get(
                    subject_identifier=child_visit.subject_identifier,
                    subject=subject)
            except DataActionItem.DoesNotExist:
                notification(
                    subject_identifier=child_visit.subject_identifier,
                    user_created=instance.user_created,
                    subject=subject,
                    comment=f'{subject}. Please capture results once available.')


@receiver(post_save, weak=False, sender=ChildPreHospitalizationInline,
          dispatch_uid='child_prev_hospitalisation_on_post_save')
def child_prev_hospitalisation_on_post_save(sender, instance, raw, created, **kwargs):
    """
       If child hospitalization has occured within the past year, put action item for
        completing INFORM instrument on redcap.
    """

    recent_year = get_utcnow() - relativedelta(years=1)

    if instance.aprox_date > recent_year.date():
        DataActionItem.objects.update_or_create(
            subject='Complete INFORM CRF on REDCap',
            subject_identifier=instance.subject_identifier,
            assigned='clinic',
            comment=('''Child was hospitalised within the past year,
                        please complete INFORM CRF on REDCAP.''')
        )


@receiver(post_save, weak=False, sender=ChildClinicalMeasurements,
          dispatch_uid='child_clinical_measurements_on_post_save')
def child_clinical_measurements_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw:
        caregiver_child_consent_cls = django_apps.get_model(
            'flourish_caregiver.caregiverchildconsent')
        matrix_pool_cls = django_apps.get_model('pre_flourish.matrixpool')

        caregiver_child_consent_obj = caregiver_child_consent_cls.objects.filter(
            subject_identifier=instance.child_visit.subject_identifier
        ).latest('version')

        match_helper = MatchHelper()
        bmi = instance.child_weight_kg / ((instance.child_height / 100) ** 2)
        bmi_group = match_helper.bmi_group(bmi)
        _age = match_helper.calculate_age(
            caregiver_child_consent_obj.child_dob)
        age_range = match_helper.age_range(_age)
        gender = 'male' if caregiver_child_consent_obj.gender == MALE else 'female'

        if bmi_group and age_range:
            heu_matrix_group_count = matrix_pool_cls.objects.filter(
                pool='heu', bmi_group=bmi_group, age_group=str(age_range),
                gender_group=gender
            ).count()
            huu_matrix_group = matrix_pool_cls.objects.filter(
                pool='huu', bmi_group=bmi_group, age_group=str(age_range),
                gender_group=gender
            )
            if heu_matrix_group_count == 0 and huu_matrix_group.count() > 0:
                match_helper.create_new_matrix_pool(
                    pool='heu', bmi_group=bmi_group, age_group=str(age_range),
                    gender_group=gender,
                    subject_identifier=instance.child_visit.subject_identifier)
                match_helper.send_email_to_pre_flourish_users(huu_matrix_group)


@receiver(post_save, weak=False, sender=ChildOffSchedule,
          dispatch_uid='child_off_schedule_on_post_save')
def child_take_off_schedule(sender, instance, raw, created, **kwargs):
    helper_cls = ChildOnScheduleHelper()
    for visit_schedule in site_visit_schedules.visit_schedules.values():
        for schedule in visit_schedule.schedules.values():
            onschedule_model_obj = helper_cls.get_onschedule_model_obj(
                schedule, query_value=instance.subject_identifier)
            if (onschedule_model_obj
                    and onschedule_model_obj.schedule_name == instance.schedule_name):
                _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
                    onschedule_model=onschedule_model_obj._meta.label_lower,
                    name=instance.schedule_name)
                schedule.take_off_schedule(
                    subject_identifier=instance.subject_identifier,
                    offschedule_datetime=instance.offschedule_datetime,
                    schedule_name=instance.schedule_name)


@receiver(post_save, weak=False, sender=ChildContinuedConsent,
          dispatch_uid='child_continued_consent_on_post_save')
def child_continued_consent_post_save(sender, instance, raw, created, **kwargs):
    child_subject_identifier = instance.subject_identifier

    caregiver_subject_identifier = child_utils.caregiver_subject_identifier(
        child_subject_identifier)

    if instance.include_contact_details == NO:

        trigger_action_item(
            model_cls=YoungAdultLocator,
            action_name=YOUNG_ADULT_LOCATOR_ACTION,
            subject_identifier=child_subject_identifier,
            repeat=False
        )

    else:

        caregiver_locator_cls = django_apps.get_model(
            'flourish_caregiver.caregiverlocator')

        try:
            caregiver_locator_obj = caregiver_locator_cls.objects.get(
                subject_identifier=caregiver_subject_identifier)

        except caregiver_locator_cls.DoesNotExist:
            pass
        else:

            assent = child_utils.child_assent_obj(child_subject_identifier)

            fields = [
                'indirect_contact_cell',
                'indirect_contact_cell_alt',
                'indirect_contact_name',
                'indirect_contact_phone',
                'indirect_contact_physical_address',
                'indirect_contact_relation',
                'locator_date',
                'mail_address',
                'may_call',
                'may_call_work',
                'may_contact_indirectly',
                'may_sms',
                'may_visit_home',
                'physical_address',
                'subject_cell',
                'subject_cell_alt',
                'subject_identifier',
                'subject_phone',
                'subject_phone_alt',
                'subject_work_cell',
                'subject_work_phone',
                'subject_work_place',
            ]

            locator_dict = model_to_dict(
                caregiver_locator_obj, fields=fields
            )

            locator_dict['subject_identifier'] = child_subject_identifier
            locator_dict['first_name'] = assent.first_name
            locator_dict['last_name'] = assent.last_name

            YoungAdultLocator.objects.update_or_create(**locator_dict)

    if instance.along_side_caregiver == NO:

        subject_history_cls = django_apps.get_model(
            'edc_visit_schedule.subjectschedulehistory')

        onschedule_models = subject_history_cls.objects.filter(
            subject_identifier=caregiver_subject_identifier,
        ).values_list('onschedule_model', flat=True)

        # get all the models
        for onschedule_model in onschedule_models:

            onschedule_model_cls = django_apps.get_model(onschedule_model)

            '''Get only on schedule model so we can filter by caregiver_subject_identifier
            and child_subject_identifier, that in turn will give us the correct schedule name a
            child is associated with'''

            schedule_objs = onschedule_model_cls.objects.filter(
                subject_identifier=caregiver_subject_identifier,
                child_subject_identifier=child_subject_identifier,
            )

            for schedule_obj in schedule_objs:

                _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
                    onschedule_model=schedule_obj._meta.label_lower,
                    name=schedule_obj.schedule_name)

                try:

                    # offschedule_datetime is equal to the crf consent_datetime
                    schedule.take_off_schedule(
                        subject_identifier=caregiver_subject_identifier,
                        offschedule_datetime=instance.consent_datetime,
                        schedule_name=schedule_obj.schedule_name)
                except InvalidOffscheduleDate:
                    pass