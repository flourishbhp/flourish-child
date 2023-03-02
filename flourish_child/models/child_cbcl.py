from django.db import models

from .child_crf_model_mixin import ChildCrfModelMixin
from ..choices import CBCL_SCALE


class ChildCBCL(ChildCrfModelMixin):

    acts_young = models.CharField(
        verbose_name='Acts too young for his/her age',
        choices=CBCL_SCALE,
        max_length=10)

    unapproved_alc_intake = models.CharField(
        verbose_name='Drinks alcohol without parents\' approval',
        choices=CBCL_SCALE,
        max_length=10)

    alc_intake_desc = models.TextField(
        verbose_name='Drinks alcohol without parents\' approval (describe)',
        max_length=500,
        blank=True, null=True)

    argues_alot = models.CharField(
        verbose_name='Argues a lot',
        choices=CBCL_SCALE,
        max_length=10)

    fails_to_finish = models.CharField(
        verbose_name='Fails to finish things he/she starts',
        choices=CBCL_SCALE,
        max_length=10)

    enjoys_little = models.CharField(
        verbose_name='There is very little he/she enjoys',
        choices=CBCL_SCALE,
        max_length=10)

    bowel_incontinence = models.CharField(
        verbose_name='Bowel movements outside toilet',
        choices=CBCL_SCALE,
        max_length=10)

    bragging = models.CharField(
        verbose_name='Bragging, boasting',
        choices=CBCL_SCALE,
        max_length=10)

    attention_deficit = models.CharField(
        verbose_name='Can\'t concentrate, can\'t pay attention for long',
        choices=CBCL_SCALE,
        max_length=10)

    obssessive = models.CharField(
        verbose_name='Can\'t get his/her mind off certain thoughts; obsessions',
        choices=CBCL_SCALE,
        max_length=10)

    obssessive_desc = models.TextField(
        verbose_name='Can\'t get his/her mind off certain thoughts; obsessions (describe)',
        max_length=500,
        blank=True, null=True)

    hyperactive = models.CharField(
        verbose_name=' Can\'t sit still, restless, or hyperactive',
        choices=CBCL_SCALE,
        max_length=10)

    too_dependent = models.CharField(
        verbose_name='Clings to adults or too dependent',
        choices=CBCL_SCALE,
        max_length=10)

    feels_lonely = models.CharField(
        verbose_name='Complains of loneliness',
        choices=CBCL_SCALE,
        max_length=10)

    confused = models.CharField(
        verbose_name='Confused or seems to be in a fog',
        choices=CBCL_SCALE,
        max_length=10)

    cries_alot = models.CharField(
        verbose_name='Cries a lot',
        choices=CBCL_SCALE,
        max_length=10)

    animal_cruelty = models.CharField(
        verbose_name='Cruel to animals',
        choices=CBCL_SCALE,
        max_length=10)

    bullies_other = models.CharField(
        verbose_name='Cruelty, bullying, or meanness to others',
        choices=CBCL_SCALE,
        max_length=10)

    daydreams = models.CharField(
        verbose_name='Daydreams or gets lost in his/her thoughts',
        choices=CBCL_SCALE,
        max_length=10)

    self_harms = models.CharField(
        verbose_name='Deliberately harms self or attempts suicide',
        choices=CBCL_SCALE,
        max_length=10)

    demands_attention = models.CharField(
        verbose_name='Demands a lot of attention',
        choices=CBCL_SCALE,
        max_length=10)

    destroys_belongings = models.CharField(
        verbose_name='Destroys his/her own things',
        choices=CBCL_SCALE,
        max_length=10)

    destroys_othr_things = models.CharField(
        verbose_name='Destroys things belonging to his/her family or others',
        choices=CBCL_SCALE,
        max_length=10)

    disobedient_home = models.CharField(
        verbose_name='Disobedient at home',
        choices=CBCL_SCALE,
        max_length=10)

    disobedient_school = models.CharField(
        verbose_name='Disobedient at school',
        choices=CBCL_SCALE,
        max_length=10)

    eating_problems = models.CharField(
        verbose_name='Doesn\'t eat well',
        choices=CBCL_SCALE,
        max_length=10)

    unfitting = models.CharField(
        verbose_name='Doesn\'t get along with other kids',
        choices=CBCL_SCALE,
        max_length=10)

    unremorseful = models.CharField(
        verbose_name='Doesn\'t seem to feel guilty after misbehaving',
        choices=CBCL_SCALE,
        max_length=10)

    easily_jealous = models.CharField(
        verbose_name='Easily jealous',
        choices=CBCL_SCALE,
        max_length=10)

    breaks_rules = models.CharField(
        verbose_name='Breaks rules at home, school, or elsewhere',
        choices=CBCL_SCALE,
        max_length=10)

    fearful = models.CharField(
        verbose_name=('Fears certain animals, situations, or places, other than '
                      'school'),
        choices=CBCL_SCALE,
        max_length=10)

    fearful_desc = models.TextField(
        verbose_name=('Fears certain animals, situations, or places, other than '
                      'school (describe)'),
        max_length=10,
        blank=True,
        null=True)

    fears_school = models.CharField(
        verbose_name='Fears going to school',
        choices=CBCL_SCALE,
        max_length=10)

    fear_harmful_thoughts = models.CharField(
        verbose_name='Fears he/she might think or do something bad',
        choices=CBCL_SCALE,
        max_length=10)

    fear_of_perfection = models.CharField(
        verbose_name='Feels he/she has to be perfect',
        choices=CBCL_SCALE,
        max_length=10)

    feels_unloved = models.CharField(
        verbose_name='Feels or complains that no one loves him/her',
        choices=CBCL_SCALE,
        max_length=10)

    feels_paranoia = models.CharField(
        verbose_name='Feels others are out to get him/her',
        choices=CBCL_SCALE,
        max_length=10)

    feels_worthless = models.CharField(
        verbose_name='Feels worthless or inferior',
        choices=CBCL_SCALE,
        max_length=10)

    accident_prone = models.CharField(
        verbose_name='Gets hurt a lot, accident-prone',
        choices=CBCL_SCALE,
        max_length=10)

    fights_involvement = models.CharField(
        verbose_name='Gets in many fights',
        choices=CBCL_SCALE,
        max_length=10)

    teased_alot = models.CharField(
        verbose_name='Gets teased a lot',
        choices=CBCL_SCALE,
        max_length=10)

    trouble_friends = models.CharField(
        verbose_name='Hangs around with others who get in trouble',
        choices=CBCL_SCALE,
        max_length=10)

    auditory_hallucination = models.CharField(
        verbose_name='Hears sounds or voices that aren\'t there',
        choices=CBCL_SCALE,
        max_length=10)

    ah_desc = models.TextField(
        verbose_name='Hears sounds or voices that aren\'t there (describe)',
        blank=True,
        null=True,
        max_length=500)

    impulsive = models.CharField(
        verbose_name='Impulsive of acts without thinking',
        choices=CBCL_SCALE,
        max_length=10)

    loner = models.CharField(
        verbose_name='Would rather be alone than with others',
        choices=CBCL_SCALE,
        max_length=10)

    cheating = models.CharField(
        verbose_name='Lying or cheating',
        choices=CBCL_SCALE,
        max_length=10)

    bites_nails = models.CharField(
        verbose_name='Bites fingernails',
        choices=CBCL_SCALE,
        max_length=10)

    nervousness = models.CharField(
        verbose_name='Nervous, highstrung, or tense',
        choices=CBCL_SCALE,
        max_length=10)

    nervous_moments = models.CharField(
        verbose_name='Nervous movements or twitching',
        choices=CBCL_SCALE,
        max_length=10)

    nervous_desc = models.TextField(
        verbose_name='Nervous movements or twitching (describe)',
        blank=True,
        null=True,
        max_length=500)

    nightmares = models.CharField(
        verbose_name='Nightmares',
        choices=CBCL_SCALE,
        max_length=10)

    disliked_by_othrs = models.CharField(
        verbose_name='Not liked by other kids',
        choices=CBCL_SCALE,
        max_length=10)

    constipated = models.CharField(
        verbose_name='Constipated, doesn\'t move bowels',
        choices=CBCL_SCALE,
        max_length=10)

    anxiousness = models.CharField(
        verbose_name='Too fearful or anxious',
        choices=CBCL_SCALE,
        max_length=10)

    feels_dizzy = models.CharField(
        verbose_name='Feels dizzy or lightheaded',
        choices=CBCL_SCALE,
        max_length=10)

    feels_guity = models.CharField(
        verbose_name='Feels too guilty',
        choices=CBCL_SCALE,
        max_length=10)

    overeating = models.CharField(
        verbose_name='Overeating',
        choices=CBCL_SCALE,
        max_length=10)

    overtired_noreason = models.CharField(
        verbose_name='Overtired without good reason',
        choices=CBCL_SCALE,
        max_length=10)

    overweight = models.CharField(
        verbose_name='Overweight',
        choices=CBCL_SCALE,
        max_length=10)

    # Physical problems without known medical cause
    body_aches = models.CharField(
        verbose_name='Aches or pains (not stomach or headaches)',
        choices=CBCL_SCALE,
        max_length=10)

    headaches = models.CharField(
        verbose_name='Headaches',
        choices=CBCL_SCALE,
        max_length=10)

    nauseous = models.CharField(
        verbose_name='Nausea, feels sick',
        choices=CBCL_SCALE,
        max_length=10)

    eye_prob = models.CharField(
        verbose_name='Problems with eyes (not if corrected by glasses',
        choices=CBCL_SCALE,
        max_length=10)

    eye_probl_desc = models.TextField(
         verbose_name='Problems with eyes (not if corrected by glasses (describe)',
         blank=True,
         null=True,
         max_length=500)

    skin_prob = models.CharField(
        verbose_name='Rashes or other skin problems',
        choices=CBCL_SCALE,
        max_length=10)

    stomach_aches = models.CharField(
        verbose_name='Stomach aches',
        choices=CBCL_SCALE,
        max_length=10)

    vomiting = models.CharField(
        verbose_name='Vomiting, throwing up',
        choices=CBCL_SCALE,
        max_length=10)

    other_phys_prob = models.CharField(
        verbose_name='Other (describe)',
        max_length=50)
    # End of section

    attacks_physical = models.CharField(
        verbose_name='Physically attacks people',
        choices=CBCL_SCALE,
        max_length=10)

    body_picking = models.CharField(
        verbose_name='Picks nose, skin, or other parts of body',
        choices=CBCL_SCALE,
        max_length=10)

    picking_desc = models.TextField(
        verbose_name='Picks nose, skin, or other parts of body (describe)',
        blank=True,
        null=True,
        max_length=500)

    sexparts_public_play = models.CharField(
        verbose_name='Plays with own sex parts in public',
        choices=CBCL_SCALE,
        max_length=10)

    sexparts_play = models.CharField(
        verbose_name='Plays with own sex parts too much',
        choices=CBCL_SCALE,
        max_length=10)

    poor_schoolwork = models.CharField(
        verbose_name='Poor school work',
        choices=CBCL_SCALE,
        max_length=10)

    clumsy = models.CharField(
        verbose_name='Poorly coordinated or clumsy',
        choices=CBCL_SCALE,
        max_length=10)

    prefers_older_kids = models.CharField(
        verbose_name='Prefers being with older kids',
        choices=CBCL_SCALE,
        max_length=10)

    prefers_young_kids = models.CharField(
        verbose_name='Prefers being with younger kids',
        choices=CBCL_SCALE,
        max_length=10)

    refuses_to_talk = models.CharField(
        verbose_name='Refuses to talk',
        choices=CBCL_SCALE,
        max_length=10)

    compulsions = models.CharField(
        verbose_name='Repeats certain acts over and over; compulsions',
        choices=CBCL_SCALE,
        max_length=10)

    compulsions_desc = models.TextField(
        verbose_name='Repeats certain acts over and over; compulsions (describe)',
        blank=True,
        null=True,
        max_length=500)

    home_runaway = models.CharField(
        verbose_name='Runs away from home',
        choices=CBCL_SCALE,
        max_length=10)

    screams_alot = models.CharField(
        verbose_name='Screams a lot',
        choices=CBCL_SCALE,
        max_length=10)

    secretive = models.CharField(
        verbose_name='Secretive, keeps things to self',
        choices=CBCL_SCALE,
        max_length=10)

    sight_hallucinations = models.CharField(
        verbose_name='Sees things that aren\'t there',
        choices=CBCL_SCALE,
        max_length=10)

    sh_desc = models.TextField(
        verbose_name='Sees things that aren\'t there (describe)',
        blank=True,
        null=True,
        max_length=500)

    self_conscious = models.CharField(
        verbose_name='Self-conscious or easily embarrassed',
        choices=CBCL_SCALE,
        max_length=10)

    sets_fires = models.CharField(
        verbose_name='Sets fires',
        choices=CBCL_SCALE,
        max_length=10)

    sexual_prob = models.CharField(
        verbose_name='Sexual problems',
        choices=CBCL_SCALE,
        max_length=10)

    sexual_prob_desc = models.TextField(
        verbose_name='Sexual problems (describe)',
        blank=True,
        null=True,
        max_length=500)

    showing_off = models.CharField(
        verbose_name='Showing off or clowning',
        choices=CBCL_SCALE,
        max_length=10)

    too_shy = models.CharField(
        verbose_name='Too shy or timid',
        choices=CBCL_SCALE,
        max_length=10)

    sleeps_less = models.CharField(
        verbose_name='Sleeps less than most kids',
        choices=CBCL_SCALE,
        max_length=10)

    sleeps_more = models.CharField(
        verbose_name='Sleeps more than most kids during day and/or night',
        choices=CBCL_SCALE,
        max_length=10)

    sleeps_more_desc = models.TextField(
        verbose_name='Sleeps more than most kids during day and/or night (describe)',
        blank=True,
        null=True,
        max_length=500)

    inattentive = models.CharField(
        verbose_name='Inattentive or easily distracted',
        choices=CBCL_SCALE,
        max_length=10)

    speech_prob = models.CharField(
        verbose_name='Speech problem',
        choices=CBCL_SCALE,
        max_length=10)

    speech_prob_desc = models.TextField(
        verbose_name='Speech problem (describe)',
        blank=True,
        null=True,
        max_length=500)

    stares_blankly = models.CharField(
        verbose_name='Stares blankly',
        choices=CBCL_SCALE,
        max_length=10)

    steals_at_home = models.CharField(
        verbose_name='Steals at home',
        choices=CBCL_SCALE,
        max_length=10)

    steals_elsewhere = models.CharField(
        verbose_name='Steals outside the home',
        choices=CBCL_SCALE,
        max_length=10)

    hoarding = models.CharField(
        verbose_name='Stores up too many things he/she doesn\'t need',
        choices=CBCL_SCALE,
        max_length=10)

    hoarding_desc = models.TextField(
        verbose_name='Stores up too many things he/she doesn\'t need (describe)',
        blank=True,
        null=True,
        max_length=500)

    strange_behavior = models.CharField(
        verbose_name='Strange behavior',
        choices=CBCL_SCALE,
        max_length=10)

    behavior_desc = models.TextField(
        verbose_name='Strange behavior (describe)',
        blank=True,
        null=True,
        max_length=500)

    strange_ideas = models.CharField(
        verbose_name='Strange ideas',
        choices=CBCL_SCALE,
        max_length=10)

    ideas_desc = models.TextField(
        verbose_name='Strange ideas (describe)',
        blank=True,
        null=True,
        max_length=500)

    irritable = models.CharField(
        verbose_name='Stubborn, sullen, or irritable',
        choices=CBCL_SCALE,
        max_length=10)

    sudden_mood_chng = models.CharField(
        verbose_name='Sudden changes in mood or feelings',
        choices=CBCL_SCALE,
        max_length=10)

    sulks_alot = models.CharField(
        verbose_name='Sulks a lot',
        choices=CBCL_SCALE,
        max_length=10)

    suspicious = models.CharField(
        verbose_name='Suspicious',
        choices=CBCL_SCALE,
        max_length=10)

    swearing = models.CharField(
        verbose_name='Swearing or obscene language',
        choices=CBCL_SCALE,
        max_length=10)

    self_harm_talks = models.CharField(
        verbose_name='Talks about killing self',
        choices=CBCL_SCALE,
        max_length=10)

    sleepwalk_talk = models.CharField(
        verbose_name='Talks or walks in sleep',
        choices=CBCL_SCALE,
        max_length=10)

    sleepwalk_desc = models.TextField(
        verbose_name='Talks or walks in sleep (describe)',
        blank=True,
        null=True,
        max_length=500)

    talks_alot = models.CharField(
        verbose_name='Talks too much',
        choices=CBCL_SCALE,
        max_length=10)

    teases_alot = models.CharField(
        verbose_name='Teases a lot',
        choices=CBCL_SCALE,
        max_length=10)

    hot_temper = models.CharField(
        verbose_name='Temper tantrum or hot temper ',
        choices=CBCL_SCALE,
        max_length=10)

    sex_thoughts = models.CharField(
        verbose_name='Thinks about sex too much',
        choices=CBCL_SCALE,
        max_length=10)

    threatens_people = models.CharField(
        verbose_name='Threatens people',
        choices=CBCL_SCALE,
        max_length=10)

    thumbsucking = models.CharField(
        verbose_name='Thumb-sucking',
        choices=CBCL_SCALE,
        max_length=10)

    smokes = models.CharField(
        verbose_name='Smokes, chews, sniffs tobacco or uses e-cigs',
        choices=CBCL_SCALE,
        max_length=10)

    trouble_sleeping = models.CharField(
        verbose_name='Trouble sleeping',
        choices=CBCL_SCALE,
        max_length=10)

    sleeping_desc = models.TextField(
        verbose_name='Trouble sleeping (describe)',
        blank=True,
        null=True,
        max_length=500)

    skips_school = models.CharField(
        verbose_name='Truancy, skips school',
        choices=CBCL_SCALE,
        max_length=10)

    underactive = models.CharField(
        verbose_name='Underactive, slow moving, or lacks energy',
        choices=CBCL_SCALE,
        max_length=10)

    unhappy = models.CharField(
        verbose_name='Unhappy, sad, or depressed',
        choices=CBCL_SCALE,
        max_length=10)

    unusually_loud = models.CharField(
        verbose_name='Unusually loud',
        choices=CBCL_SCALE,
        max_length=10)

    drug_usage = models.CharField(
        verbose_name='Uses drugs for nonmedical purposes (don\'t include alcohol or tobacco)',
        choices=CBCL_SCALE,
        max_length=10)

    drug_usage_desc = models.TextField(
        verbose_name=('Uses drugs for nonmedical purposes (don\'t include alcohol or tobacco)'
                      ' (describe)'),
        blank=True,
        null=True,
        max_length=500)

    vandalism = models.CharField(
        verbose_name='Vandalism',
        choices=CBCL_SCALE,
        max_length=10)

    daytime_wetting = models.CharField(
        verbose_name='Wets self during the day',
        choices=CBCL_SCALE,
        max_length=10)

    bedtime_wetting = models.CharField(
        verbose_name='Wets the bed',
        choices=CBCL_SCALE,
        max_length=10)

    whining = models.CharField(
        verbose_name='Whining',
        choices=CBCL_SCALE,
        max_length=10)

    gender_dissonant = models.CharField(
        verbose_name='Wishes to be of opposite sex',
        choices=CBCL_SCALE,
        max_length=10)

    withdrawn = models.CharField(
        verbose_name='Withdrawn, doesn\'t get invovled with others',
        choices=CBCL_SCALE,
        max_length=10)

    worries = models.CharField(
        verbose_name='Worries',
        choices=CBCL_SCALE,
        max_length=10)

    other_problems = models.TextField(
        verbose_name='Please write in any problems your child has that were not listed above',
        max_length=200)

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Child CBCL'
        verbose_name_plural = 'Child CBCL'
