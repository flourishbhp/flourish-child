from datetime import datetime

from dateutil.tz import gettz
from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings


class AppConfig(DjangoAppConfig):
    name = 'flourish_child'
    verbose_name = 'Flourish Child'
    admin_site_name = 'flourish_child_admin'
    start_date_year_3 = datetime(
        2022, 7, 1, 0, 0, 0, tzinfo=gettz('UTC')).date()
    end_date_year_5 = datetime(
        2025, 6, 30, 0, 0, 0, tzinfo=gettz('UTC')).date()

    consent_version = 4

    def ready(self):
        from .models import child_consent_on_post_save


if settings.APP_NAME == 'flourish_child':
    from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
    from edc_appointment.appointment_config import AppointmentConfig
    from edc_appointment.apps import AppConfig as BaseEdcAppointmentAppConfig
    from edc_appointment.constants import COMPLETE_APPT
    from edc_metadata.apps import AppConfig as BaseEdcMetadataAppConfig
    from edc_protocol.apps import AppConfig as BaseEdcProtocolAppConfigs
    from edc_facility.apps import AppConfig as BaseEdcFacilityAppConfig
    from edc_timepoint.apps import AppConfig as BaseEdcTimepointAppConfig
    from edc_timepoint.timepoint import Timepoint
    from edc_timepoint.timepoint_collection import TimepointCollection
    from edc_visit_tracking.apps import AppConfig as BaseEdcVisitTrackingAppConfig
    from edc_visit_tracking.constants import MISSED_VISIT, COMPLETED_PROTOCOL_VISIT
    from edc_visit_tracking.constants import SCHEDULED, UNSCHEDULED, LOST_VISIT
    from edc_constants.constants import FAILED_ELIGIBILITY
    from edc_senaite_interface.apps import AppConfig as BaseEdcSenaiteInterfaceAppConfig


    class EdcAppointmentAppConfig(BaseEdcAppointmentAppConfig):
        configurations = [
            AppointmentConfig(
                model='edc_appointment.appointment',
                related_visit_model='flourish_caregiver.maternalvisit',
                appt_type='clinic'),
            AppointmentConfig(
                model='pre_flourish.appointment',
                related_visit_model='pre_flourish.preflourishvisit',
                appt_type='clinic'),
            AppointmentConfig(
                model='flourish_child.appointment',
                related_visit_model='flourish_child.childvisit',
                appt_type='clinic'),
            AppointmentConfig(
                model='flourish_facet.appointment',
                related_visit_model='flourish_facet.facetvisit',
                appt_type='clinic'), ]


    class EdcMetadataAppConfig(BaseEdcMetadataAppConfig):
        reason_field = {
            'pre_flourish.preflourishvisit': 'reason',
            'flourish_caregiver.maternalvisit': 'reason',
            'flourish_child.childvisit': 'reason',
            'flourish_facet.facetvisit': 'reason', }
        create_on_reasons = [SCHEDULED, UNSCHEDULED, COMPLETED_PROTOCOL_VISIT]
        delete_on_reasons = [LOST_VISIT, MISSED_VISIT, FAILED_ELIGIBILITY]


    class EdcProtocolAppConfig(BaseEdcProtocolAppConfigs):
        protocol = 'BHP142'
        protocol_name = 'Flourish Follow'
        protocol_number = '142'
        protocol_title = ''
        study_open_datetime = datetime(
            2020, 8, 14, 0, 0, 0, tzinfo=gettz('UTC'))
        study_close_datetime = datetime(
            2026, 8, 13, 23, 59, 59, tzinfo=gettz('UTC'))


    class EdcTimepointAppConfig(BaseEdcTimepointAppConfig):
        timepoints = TimepointCollection(
            timepoints=[
                Timepoint(
                    model='edc_appointment.appointment',
                    datetime_field='appt_datetime',
                    status_field='appt_status',
                    closed_status=COMPLETE_APPT),
                Timepoint(
                    model='edc_appointment.historicalappointment',
                    datetime_field='appt_datetime',
                    status_field='appt_status',
                    closed_status=COMPLETE_APPT),
                Timepoint(
                    model='flourish_child.appointment',
                    datetime_field='appt_datetime',
                    status_field='appt_status',
                    closed_status=COMPLETE_APPT),
                Timepoint(
                    model='flourish_child.historicalappointment',
                    datetime_field='appt_datetime',
                    status_field='appt_status',
                    closed_status=COMPLETE_APPT),
                Timepoint(
                    model='pre_flourish.appointment',
                    datetime_field='appt_datetime',
                    status_field='appt_status',
                    closed_status=COMPLETE_APPT),
                Timepoint(
                    model='flourish_facet.appointment',
                    datetime_field='appt_datetime',
                    status_field='appt_status',
                    closed_status=COMPLETE_APPT),
            ])


    class EdcVisitTrackingAppConfig(BaseEdcVisitTrackingAppConfig):
        visit_models = {
            'flourish_caregiver': (
                'maternal_visit', 'flourish_caregiver.maternalvisit'),
            'flourish_child': (
                'child_visit', 'flourish_child.childvisit'),
            'pre_flourish': (
                'pre_flourish_visit', 'pre_flourish.preflourishvisit'),
            'flourish_facet': (
                'facet_visit', 'flourish_facet.facetvisit'), }


    class EdcFacilityAppConfig(BaseEdcFacilityAppConfig):
        country = 'botswana'
        definitions = {
            '7-day clinic': dict(days=[MO, TU, WE, TH, FR, SA, SU],
                                 slots=[100, 100, 100, 100, 100, 100, 100]),
            '5-day clinic': dict(days=[MO, TU, WE, TH, FR],
                                 slots=[100, 100, 100, 100, 100])}


    class EdcSenaiteInterfaceAppConfig(BaseEdcSenaiteInterfaceAppConfig):
        host = "https://bhplims.bhp.org.bw"
        client = "Testing"
        courier = "ABRAHAM MAIGWA"
        sample_type_match = {'humoral_immunogenicity': 'Serum',
                             'sars_serum': 'Serum',
                             'sars_cov2_pcr': 'Swab',
                             'hematology': 'Whole Blood EDTA',
                             'wb_cmi': 'Whole Blood EDTA',
                             'urine_hcg': 'Urine'}
        container_type_match = {'humoral_immunogenicity': 'Cryogenic vial',
                                'sars_cov2_serology': 'Cryogenic vial',
                                'sars_cov2_pcr': 'Cryogenic Vial',
                                'hematology': 'EDTA Tube',
                                'wb_cmi': 'EDTA Tube',
                                'urine_hcg': 'Urine Cup'}
        template_match = {'humoral_immunogenicity': 'Serum storage',
                          'sars_serum': 'SARS-CoV-2 serology',
                          'sars_cov2_pcr': 'SARS COV 2 PCR',
                          'hematology': 'CBC',
                          'wb_cmi': 'PBMC Whole Blood EDTA',
                          'urine_hcg': 'Urine HCG'}
