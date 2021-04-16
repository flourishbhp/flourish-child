from django.db import models
from edc_constants.choices import YES_NO

from .child_crf_model_mixin import ChildCrfModelMixin
from ..choices import DEPRESSION_SCALE, DIFFICULTY_LEVEL


class ChildPhqDepressionScreening(ChildCrfModelMixin):

    depressed = models.CharField(
        verbose_name='Feeling down, depressed, irritable or hopelesss',
        choices=DEPRESSION_SCALE,
        max_length=25, )

    activity_interest = models.CharField(
        verbose_name='Little interest or pleasure in doing things',
        choices=DEPRESSION_SCALE,
        max_length=25, )

    sleep_disorders = models.CharField(
        verbose_name='Trouble falling, staying asleep or sleeping too much?',
        choices=DEPRESSION_SCALE,
        max_length=25, )

    eating_disorders = models.CharField(
        verbose_name='Poor appetite or overeating',
        choices=DEPRESSION_SCALE,
        max_length=25, )

    fatigued = models.CharField(
        verbose_name='Feeling tired or having little energy',
        choices=DEPRESSION_SCALE,
        max_length=25, )

    self_doubt = models.CharField(
        verbose_name=('Feeling bad about yourself or that you are a failure or'
                      ' have let yourself or your family down'),
        choices=DEPRESSION_SCALE,
        max_length=25, )

    easily_distracted = models.CharField(
        verbose_name=('Trouble concentrating on things, such as reading the '
                      'newspaper or watching TV.'),
        choices=DEPRESSION_SCALE,
        max_length=25, )

    restlessness = models.CharField(
        verbose_name=('Moving or speaking so slowly that other people could '
                      'have noticed. Or the opposite; being so fidgety or '
                      'restless that you have been moving around a lot more than usual'),
        choices=DEPRESSION_SCALE,
        max_length=25, )

    self_harm = models.CharField(
        verbose_name=('Thoughts that you would be better off dead or of '
                      'hurting yourself in some way'),
        choices=DEPRESSION_SCALE,
        max_length=25, )

    felt_depressed = models.CharField(
        max_length=3,
        verbose_name=('In the past year have you felt depressed or sad most '
                      'days, even if you felt okay sometimes'),
        choices=YES_NO)

    problems_effect = models.CharField(
        verbose_name=('If you are experiencing any of the problems on this form, '
                      'how difficult have these problems made it for you to do '
                      'your work, take care of things at home or get along with other people?'),
        choices=DIFFICULTY_LEVEL,
        max_length=30)

    self_harm_thoughts = models.CharField(
        max_length=3,
        verbose_name=('Has there been a time in the past month when you have '
                      'had serious thoughts about ending your life?'),
        choices=YES_NO)

    suidice_attempt = models.CharField(
        max_length=3,
        verbose_name=('Have you EVER, in your WHOLE LIFE, tried to kill yourself '
                      'or made a suicide attempt? '),
        choices=YES_NO)

    depression_score = models.IntegerField(
        verbose_name='Depression score',
        default="",
        null=True,
        blank=True)

    def save(self, *args, **kwargs):
        self.depression_score = self.calculate_depression_score()
        super().save(*args, **kwargs)

    def calculate_depression_score(self):
        score = 0
        for f in self._meta.get_fields():
            if f.name in ['activity_interest', 'depressed', 'sleep_disorders',
                          'fatigued', 'eating_disorders', 'self_doubt',
                          'easily_distracted', 'restlessness', 'self_harm',
                          'felt_depressed', 'problems_effect', 'self_harm_thoughts',
                          'suidice_attempt']:
                score += int(getattr(self, f.name))
        return score

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Child PHQ Depression Screening'
        verbose_name_plural = 'Child PHQ Depression Screening'
