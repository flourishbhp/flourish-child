from collections import OrderedDict
from django.conf import settings
from django.contrib import admin
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from edc_consent.actions import (
    flag_as_verified_against_paper, unflag_as_verified_against_paper)
from edc_model_admin import ModelAdminNextUrlRedirectError, audit_fieldset_tuple, audit_fields
from simple_history.admin import SimpleHistoryAdmin

from ..admin_site import flourish_child_admin
from ..forms import ChildAssentForm
from ..models import ChildAssent
from .model_admin_mixins import ModelAdminMixin


@admin.register(ChildAssent, site=flourish_child_admin)
class ChildAssentAdmin(ModelAdminMixin, SimpleHistoryAdmin, admin.ModelAdmin):

    form = ChildAssentForm

    fieldsets = (
        (None, {
            'fields': (
                'screening_identifier',
                'subject_identifier',
                'first_name',
                'last_name',
                'initials',
                'language',
                'is_literate',
                'witness_name',
                'dob',
                'is_dob_estimated',
                'citizen',
                'gender',
                'identity',
                'identity_type',
                'confirm_identity',
                'hiv_testing',
                'remain_in_study',
                'preg_testing')}),
        ('Review Questions', {
            'fields': (
                'consent_reviewed',
                'study_questions',
                'assessment_score',
                'consent_signature',
                'consent_copy',
                'specimen_consent',
                'consent_datetime'),
            'description': 'The following questions are directed to the interviewer.'}),
        audit_fieldset_tuple)

    radio_fields = {
        'gender': admin.VERTICAL,
        'assessment_score': admin.VERTICAL,
        'citizen': admin.VERTICAL,
        'consent_copy': admin.VERTICAL,
        'consent_reviewed': admin.VERTICAL,
        'consent_signature': admin.VERTICAL,
        'is_dob_estimated': admin.VERTICAL,
        'identity_type': admin.VERTICAL,
        'is_literate': admin.VERTICAL,
        'language': admin.VERTICAL,
        'study_questions': admin.VERTICAL,
        'remain_in_study': admin.VERTICAL,
        'hiv_testing': admin.VERTICAL,
        'preg_testing': admin.VERTICAL,
        'specimen_consent': admin.VERTICAL, }

    list_display = ('subject_identifier',
                    'verified_by',
                    'is_verified',
                    'is_verified_datetime',
                    'first_name',
                    'initials',
                    'gender',
                    'dob',
                    'consent_datetime',
                    'created',
                    'modified',
                    'user_created',
                    'user_modified')

    list_filter = ('is_verified',
                   'remain_in_study',
                   'hiv_testing',
                   'preg_testing',
                   'gender',
                   'identity_type')
    search_fields = ('subject_identifier', 'dob',)

    def redirect_url(self, request, obj, post_url_continue=None):
        redirect_url = super().redirect_url(
            request, obj, post_url_continue=post_url_continue)
        if request.GET.dict().get('next'):
            url_name = settings.DASHBOARD_URL_NAMES.get('child_dashboard_url')
            attrs = ['subject_identifier', ]
            options = {k: request.GET.dict().get(k)
                       for k in attrs if request.GET.dict().get(k)}
            options.update(subject_identifier=obj.subject_identifier)
            try:
                redirect_url = reverse(url_name, kwargs=options)
            except NoReverseMatch as e:
                raise ModelAdminNextUrlRedirectError(
                    f'{e}. Got url_name={url_name}, kwargs={options}.')
        return redirect_url

    def get_actions(self, request):

        super_actions = super().get_actions(request)

        if ('flourish_child.change_childassent'
                in request.user.get_group_permissions()):

            consent_actions = [
                flag_as_verified_against_paper,
                unflag_as_verified_against_paper]

            # Add actions from this ModelAdmin.
            actions = (self.get_action(action) for action in consent_actions)
            # get_action might have returned None, so filter any of those out.
            actions = filter(None, actions)

            actions = self._filter_actions_by_permissions(request, actions)
            # Convert the actions into an OrderedDict keyed by name.
            actions = OrderedDict(
                (name, (func, name, desc))
                for func, name, desc in actions
            )

            super_actions.update(actions)

        return super_actions

    def get_readonly_fields(self, request, obj=None):
        return (super().get_readonly_fields(request, obj=obj)
                + audit_fields)
