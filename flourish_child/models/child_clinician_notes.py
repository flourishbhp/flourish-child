import mimetypes
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy
from edc_base.model_mixins import BaseUuidModel
from edc_base.utils import get_utcnow
from edc_consent.field_mixins import VerificationFieldsMixin

from .child_crf_model_mixin import ChildCrfModelMixin


# Define a custom validator
def validate_image_or_pdf(file):
    # Check file type (you can extend this logic for more file types)
    valid_image_types = ['image/jpeg', 'image/png', 'image/gif']
    valid_pdf_type = 'application/pdf'
    file_type, _ = mimetypes.guess_type(file.name)

    if (file_type not in valid_image_types and
            file_type != valid_pdf_type):
        raise ValidationError(
            gettext_lazy('Only image files and PDF files are allowed.'))


class ChildClinicianNotes(VerificationFieldsMixin, ChildCrfModelMixin):
    crf_date_validator_cls = None

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Infant/Child/Adolescent Clinician Notes'
        verbose_name_plural = 'Infant/Child/Adolescent Clinician Notes'


class ClinicianNotesImage(BaseUuidModel):
    clinician_notes = models.ForeignKey(
        ChildClinicianNotes,
        on_delete=models.PROTECT,
        related_name='child_clinician_notes', )

    image = models.FileField(
        upload_to='child_notes/',
        validators=[validate_image_or_pdf])

    user_uploaded = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='user uploaded', )
    datetime_captured = models.DateTimeField(
        default=get_utcnow)

    def clinician_notes_image(self):
        # Get the file type
        file_url = getattr(self.image, 'url', None)
        file_type, _ = mimetypes.guess_type(file_url)

        # Check if it's an image
        if file_type:
            if file_type.startswith('image'):
                return mark_safe(
                    f'<a href="{file_url}" target="_blank">'
                    f'<img src="{file_url}" style="padding-right:150px" width="150" height="100" />'
                    '</a>'
                )
            # If it's a PDF (or other file type)
            elif file_type == 'application/pdf':
                return mark_safe(
                    f'<a href="{file_url}" target="_blank">View PDF</a>'
                )
            else:
                return mark_safe('-')

    clinician_notes_image.short_description = 'Clinician Notes Image'
    clinician_notes_image.allow_tags = True
