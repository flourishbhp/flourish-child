from django.forms import model_to_dict
from django.http import JsonResponse
from urllib.parse import urlparse, parse_qs

from .models import VaccinesReceived


def get_received_dates(request, vaccine):
    subject_identifier = None
    referrer = request.META.get('HTTP_REFERER')
    if referrer:
        parsed_referrer = urlparse(referrer)
        referrer_params = parse_qs(parsed_referrer.query)
        subject_identifier = referrer_params.get('subject_identifier', None)[0]
    data = {}
    try:
        data = VaccinesReceived.objects.filter(
            child_immunization_history__child_visit__subject_identifier=subject_identifier,
            received_vaccine_name=vaccine).latest('child_immunization_history__report_datetime')
    except VaccinesReceived.DoesNotExist:
        pass
    else:
        data_dict = model_to_dict(data, fields=['first_dose_dt', 'second_dose_dt', 'third_dose_dt'])
        return JsonResponse(data_dict)
    return JsonResponse(data)
