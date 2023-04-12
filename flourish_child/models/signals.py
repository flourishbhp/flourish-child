import os
from datetime import datetime

import PIL
import pyminizip
import pypdfium2 as pdfium
from PIL import Image
from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from edc_action_item.site_action_items import site_action_items
from edc_base.utils import age, get_utcnow
from edc_constants.constants import OPEN, NEW, POS, NO, YES, NEG, IND, UNKNOWN
from edc_data_manager.models import DataActionItem
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from flourish_child.models.child_birth import ChildBirth
from flourish_prn.action_items import CHILD_DEATH_REPORT_ACTION, TB_ADOL_STUDY_ACTION
from flourish_prn.models.child_death_report import ChildDeathReport

from flourish_child.models.tb_adol_assent import TbAdolAssent
from flourish_child.models.adol_tb_lab_results import TbLabResultsAdol
from flourish_child.models.adol_hiv_testing import HivTestingAdol
from flourish_child.models.adol_tb_presence_household_member import \
    TbPresenceHouseholdMembersAdol
from flourish_child.models.tb_visit_screen_adol import TbVisitScreeningAdolescent
from flourish_prn.models.tb_adol_off_study import TBAdolOffStudy
from .child_assent import ChildAssent
from .child_clinician_notes import ClinicianNotesImage
from .child_dummy_consent import ChildDummySubjectConsent
from .child_visit import ChildVisit
from ..models import ChildOffSchedule, AcademicPerformance, ChildSocioDemographic
from ..models import ChildPreHospitalizationInline
from ..helper_classes import ChildFollowUpBookingHelper


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
                            version=instance.version)
                    else:
                        caregiver_prev_enrolled_cls = django_apps.get_model(
                            'flourish_caregiver.caregiverpreviouslyenrolled')
                        try:
                            caregiver_prev_enrolled_cls.objects.get(
                                subject_identifier=instance.subject_identifier[:-3])
                        except caregiver_prev_enrolled_cls.DoesNotExist:
                            pass
                        else:
                            dummy_consent_obj.save()

                        caregiver_child_consent_obj.subject_identifier = \
                            instance.subject_identifier
                        caregiver_child_consent_obj.save(
                            update_fields=['subject_identifier', 'modified',
                                           'user_modified'])


@receiver(post_save, weak=False, sender=ChildDummySubjectConsent,
          dispatch_uid='child_consent_on_post_save')
def child_consent_on_post_save(sender, instance, raw, created, **kwargs):
    """Put subject on cohort a schedule after consenting.
    """
    if not raw:

        caregiver_prev_enrolled_cls = django_apps.get_model(
            'flourish_caregiver.caregiverpreviouslyenrolled')
        try:
            prev_enrolled = caregiver_prev_enrolled_cls.objects.get(
                subject_identifier=instance.subject_identifier[:-3])
        except caregiver_prev_enrolled_cls.DoesNotExist:
            pass
        else:
            put_cohort_onschedule(instance.cohort, instance=instance,
                                  base_appt_datetime=prev_enrolled.report_datetime)

        maternal_delivery_cls = django_apps.get_model(
            'flourish_caregiver.maternaldelivery')
        try:
            maternal_delivery_obj = maternal_delivery_cls.objects.get(
                delivery_datetime=instance.consent_datetime,
                subject_identifier=instance.subject_identifier[:-3])
        except maternal_delivery_cls.DoesNotExist:
            pass
        else:
            put_on_schedule((instance.cohort + '_birth'), instance=instance,
                            base_appt_datetime=maternal_delivery_obj.created)


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
    - Put subject on quarterly schedule at enrollment visit.
    """
    if getattr(instance, 'survival_status') == 'dead':
        trigger_action_item(ChildDeathReport, CHILD_DEATH_REPORT_ACTION,
                            instance.subject_identifier,
                            repeat=True)

    if not raw and created and instance.visit_code in ['2000', '2000D', '3000']:

        if 'sec' in instance.schedule_name:

            cohort_list = instance.schedule_name.split('_')

            cohort = '_'.join(['cohort', cohort_list[1], 'sec_qt'])
        elif 'fu' in instance.schedule_name:

            cohort_list = instance.schedule_name.split('_')

            cohort = '_'.join(['cohort', cohort_list[1], 'fu_qt'])
        else:
            cohort_list = instance.schedule_name.split('_')

            cohort = '_'.join(['cohort', cohort_list[1], 'quarterly'])

        put_on_schedule(cohort, instance=instance,
                        subject_identifier=instance.subject_identifier,
                        base_appt_datetime=instance.report_datetime.replace(
                            microsecond=0))


@receiver(post_save, weak=False, sender=TbAdolAssent,
          dispatch_uid='tb_adol_on_post_save')
def tb_adol_assent_on_post_save(sender, instance, raw, created, **kwargs):
    if instance.is_eligible:
        put_on_schedule('tb_adol', instance=instance,
                        subject_identifier=instance.subject_identifier,
                        base_appt_datetime=instance.consent_datetime.replace(
                            microsecond=0))


@receiver(post_save, weak=False, sender=ChildBirth,
          dispatch_uid='child_visit_on_post_save')
def child_birth_on_post_save(sender, instance, raw, created, **kwargs):
    """
    - Put subject on birth schedule.
    """
    if not raw and created:
        maternal_delivery_cls = django_apps.get_model(
            'flourish_caregiver.maternaldelivery')

        base_appt_datetime = None
        try:
            maternal_delivery_obj = maternal_delivery_cls.objects.get(
                subject_identifier=instance.subject_identifier[:-3])
        except maternal_delivery_cls.DoesNotExist:
            pass
        else:
            if maternal_delivery_obj.live_infants_to_register == 1:
                base_appt_datetime = maternal_delivery_obj.delivery_datetime.replace(
                    microsecond=0)
                put_on_schedule(
                    'child_cohort_a_birth', instance=instance,
                    subject_identifier=instance.subject_identifier,
                    base_appt_datetime=base_appt_datetime)

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


def notification(subject_identifier, subject, user_created,
                 group_names=('assignable users',)):
    if user_created:
        try:
            user = User.objects.get(username=user_created)
        except User.DoesNotExist:
            pass
        else:
            try:
                user.groups.get(name__in=group_names)
            except Group.DoesNotExist:
                groups = Group.objects.filter(name__in=group_names)
                for group in groups:
                    user.groups.add(group)
                user.save()
            finally:
                DataActionItem.objects.create(
                    subject_identifier=subject_identifier,
                    user_created=user_created,
                    status=OPEN,
                    action_priority='high',
                    assigned=user.username,
                    subject=subject)


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
            subject='Complete INFROM CRF on REDCap',
            subject_identifier=instance.subject_identifier,
            assigned='clinic',
            comment=('''Child was hospitalised within the past year,
                        please complete INFORM CRF on REDCAP.''')
        )


def put_cohort_onschedule(cohort, instance, base_appt_datetime=None):
    if cohort:
        instance.registration_update_or_create()
        if 'sec' in cohort or 'pool' in cohort:
            put_on_schedule(cohort, instance=instance,
                            base_appt_datetime=base_appt_datetime)
        else:
            put_on_schedule(cohort + '_enrol', instance=instance,
                            base_appt_datetime=base_appt_datetime)
            # put_on_schedule(cohort + '_quart', instance=instance,
            # base_appt_datetime=base_appt_datetime)
        # put_on_schedule(cohort + '_fu', instance=instance,
        # base_appt_datetime=django_apps.get_app_config(
        # 'edc_protocol').study_open_datetime)


def put_on_schedule(cohort, instance=None, subject_identifier=None,
                    base_appt_datetime=None):
    if instance:
        subject_identifier = subject_identifier or instance.subject_identifier

        cohort_label_lower = ''.join(cohort.split('_'))

        if 'fuqt' in cohort_label_lower:
            cohort_label_lower = cohort_label_lower.replace('fuqt', 'fuquart')

        if 'enrol' in cohort:
            cohort_label_lower = cohort_label_lower.replace(
                'enrol', 'enrollment')

        elif 'sec' in cohort:
            cohort_label_lower = cohort_label_lower.replace('qt', 'quart')

        if 'birth' in cohort:
            onschedule_model = 'flourish_child.onschedule' + cohort_label_lower
            schedule_name = cohort.replace('cohort_', '') + '_schedule1'
        else:
            onschedule_model = 'flourish_child.onschedulechild' + cohort_label_lower

            schedule_name = cohort.replace('cohort', 'child') + '_schedule1'

        if 'quarterly' in cohort:
            schedule_name = schedule_name.replace('quarterly', 'quart')

        if 'tb_adol' in cohort:
            schedule_name = 'tb_adol_schedule'
            onschedule_model = 'flourish_child.onschedulechildtbadolschedule'

        _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            onschedule_model=onschedule_model, name=schedule_name)

        schedule.put_on_schedule(
            subject_identifier=subject_identifier,
            onschedule_datetime=base_appt_datetime,
            schedule_name=schedule_name,
            base_appt_datetime=base_appt_datetime)

        if 'enrol' in cohort and 'sec' not in cohort:
            # book participant for followup
            booking_helper = ChildFollowUpBookingHelper()
            booking_dt = base_appt_datetime + relativedelta(years=1)
            booking_helper.schedule_fu_booking(subject_identifier, booking_dt)


def trigger_action_item(model_cls, action_name, subject_identifier, repeat=False):
    action_cls = site_action_items.get(
        model_cls.action_name)
    action_item_model_cls = action_cls.action_item_model_cls()

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


@receiver(post_save, weak=False, sender=ChildOffSchedule,
          dispatch_uid='child_off_schedule_on_post_save')
def child_take_off_schedule(sender, instance, raw, created, **kwargs):
    for visit_schedule in site_visit_schedules.visit_schedules.values():
        for schedule in visit_schedule.schedules.values():
            onschedule_model_obj = get_child_onschedule_model_obj(
                schedule, instance.subject_identifier)
            if (onschedule_model_obj
                    and onschedule_model_obj.schedule_name == instance.schedule_name):
                _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
                    onschedule_model=onschedule_model_obj._meta.label_lower,
                    name=instance.schedule_name)
                schedule.take_off_schedule(
                    subject_identifier=instance.subject_identifier,
                    offschedule_datetime=instance.offschedule_datetime,
                    schedule_name=instance.schedule_name)


def get_caregiver_onschedule_model_obj(schedule, subject_identifier):
    try:
        return schedule.onschedule_model_cls.objects.get(
            child_subject_identifier=subject_identifier)
    except ObjectDoesNotExist:
        return None


def get_child_onschedule_model_obj(schedule, subject_identifier):
    try:
        return schedule.onschedule_model_cls.objects.get(
            subject_identifier=subject_identifier)
    except ObjectDoesNotExist:
        return None


def consent_version(subject_identifier):
    preg_subject_screening_cls = django_apps.get_model(
        'flourish_caregiver.screeningpregwomen')
    prior_subject_screening_cls = django_apps.get_model(
        'flourish_caregiver.screeningpriorbhpparticipants')

    consent_version_cls = django_apps.get_model(
        'flourish_caregiver.flourishconsentversion')

    subject_screening_obj = None

    try:
        subject_screening_obj = preg_subject_screening_cls.objects.get(
            subject_identifier=subject_identifier[:-3])

    except preg_subject_screening_cls.DoesNotExist:

        try:
            subject_screening_obj = prior_subject_screening_cls.objects.get(
                subject_identifier=subject_identifier[:-3])

        except prior_subject_screening_cls.DoesNotExist:
            raise ValidationError(
                'Missing Subject Screening form. Please complete '
                'it before proceeding.')

    if subject_screening_obj:
        try:
            consent_version_obj = consent_version_cls.objects.get(
                screening_identifier=subject_screening_obj.screening_identifier)
        except consent_version_cls.DoesNotExist:
            raise ValidationError(
                'Missing Consent Version form. Please complete '
                'it before proceeding.')
        return consent_version_obj.version


def encrypt_files(instance, subject_identifier):
    base_path = settings.MEDIA_ROOT
    if instance.image:
        upload_to = f'{instance.image.field.upload_to}'
        timestamp = datetime.timestamp(get_utcnow())
        zip_filename = f'{subject_identifier}_{timestamp}.zip'
        with open('filekey.key', 'r') as filekey:
            key = filekey.read().rstrip()
        com_lvl = 8
        pyminizip.compress(f'{instance.image.path}', None,
                           f'{base_path}/{upload_to}{zip_filename}', key, com_lvl)
    # remove unencrypted file
    if os.path.exists(f'{instance.image.path}'):
        os.remove(f'{instance.image.path}')
    instance.image = f'{upload_to}{zip_filename}'
    instance.save()


def stamp_image(instance):
    filefield = instance.image
    filename = filefield.name  # gets the "normal" file name as it was uploaded
    storage = filefield.storage
    path = storage.path(filename)
    if '.pdf' not in path:
        base_image = Image.open(path)
        stamped_img = add_image_stamp(base_image=base_image)
        stamped_img.save(path)
    else:
        print_pdf(path)


def add_image_stamp(base_image=None, position=(25, 25), resize=(500, 500)):
    """
    Superimpose image of a stamp over copy of the base image
    @param image_path: dir to base image
    @param dont_save: boolean for not saving the image just converting
    @param position: pixels(w,h) to superimpose stamp at
    """
    stamp = Image.open('media/stamp/true-copy.png')
    if resize:
        stamp = stamp.resize(resize, PIL.Image.ANTIALIAS)

    width, height = base_image.size
    stamp_width, stamp_height = stamp.size

    # Determine orientation of the base image before pasting stamp
    if width < height:
        pos_width = round(width / 2) - round(stamp_width / 2)
        pos_height = height - stamp_height
        position = (pos_width, pos_height)
    elif width > height:
        stamp = stamp.rotate(90)
        pos_width = width - stamp_width
        pos_height = round(height / 2) - round(stamp_height / 2)
        position = (pos_width, pos_height)

    # paste stamp over image
    base_image.paste(stamp, position, mask=stamp)
    return base_image


def print_pdf(filepath):
    pdf = pdfium.PdfDocument(filepath)
    page_indices = [i for i in range(len(pdf))]
    renderer = pdf.render_to(
        pdfium.BitmapConv.pil_image,
        page_indices=page_indices,
        scale=300 / 72
    )
    stamped_pdf_images = []
    for image, index in zip(renderer, page_indices):
        stamped_pdf_images.append(add_image_stamp(base_image=image))
    first_img = stamped_pdf_images[0]
    first_img.save(filepath, save_all=True,
                   append_images=stamped_pdf_images[1:])


def put_child_offschedule(subject_identifier, schedule_name):
    if not (subject_identifier or schedule_name):
        raise Exception("Subject identifier or schedule name cannot be empty")

    try:
        offschedule_obj = ChildOffSchedule.objects.get(
            subject_identifier=subject_identifier,
            schedule_name=schedule_name)
    except ChildOffSchedule.DoesNotExist:
        ChildOffSchedule.objects.create(
            subject_identifier=subject_identifier,
            schedule_name=schedule_name,
            offschedule_datetime=get_utcnow())
    else:
        offschedule_obj.save()
