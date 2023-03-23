from django.forms import model_to_dict
from django.http import JsonResponse
from urllib.parse import urlparse, parse_qs

from .models import VaccinesReceived


def get_received_dates(request, vaccine):
    """ Query vaccines received to retrieve vaccination date(s) for a participant's
        selected vaccine and return the JSON response for the dates.
        @param request:  request object
        @param vaccine: selected vaccine name
        @return: JSON response object with the corresponding vaccine dates.
    """
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
        data_dict = model_to_dict(
            data, fields=['first_dose_dt', 'second_dose_dt', 'third_dose_dt',
                          'booster_dose_dt', 'booster_2nd_dose_dt', 'booster_3rd_dose_dt'])
        return JsonResponse(data_dict)
    return JsonResponse(data)
