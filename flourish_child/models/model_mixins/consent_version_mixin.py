from ...helper_classes.utils import child_utils


class ConsentVersionModelModelMixin:

    """ Base model for all models
    """

    def get_consent_version(self):
        return child_utils.consent_version(
            subject_identifier=self.subject_identifier)

    def save(self, *args, **kwargs):
        self.consent_version = self.get_consent_version()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True