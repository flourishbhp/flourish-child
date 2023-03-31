from django.apps import apps as django_apps
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError


class IntvUsersMixin:
    @property
    def intv_users(self):
        """Return a list of users that can be assigned an issue.
        """
        intv_choices = ()
        user = django_apps.get_model('auth.user')
        app_config = django_apps.get_app_config('flourish_caregiver')
        interviewers_group = app_config.interviewers_group
        try:
            Group.objects.get(name=interviewers_group)
        except Group.DoesNotExist:
            pass

        interviewers = user.objects.filter(
            groups__name=interviewers_group)
        extra_choices = ()
        if app_config.extra_assignee_choices:
            for _, value in app_config.extra_assignee_choices.items():
                extra_choices += (value[0],)
        for intv in interviewers:
            username = intv.username
            if not intv.first_name:
                raise ValidationError(
                    f"The user {username} needs to set their first name.")
            if not intv.last_name:
                raise ValidationError(
                    f"The user {username} needs to set their last name.")
            full_name = (f'{intv.first_name} '
                         f'{intv.last_name}')
            intv_choices += ((username, full_name),)
        if extra_choices:
            intv_choices += extra_choices
        return intv_choices
