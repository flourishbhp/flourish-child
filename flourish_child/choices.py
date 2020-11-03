from edc_constants.constants import FAILED_ELIGIBILITY, YES, NO, OTHER, ON_STUDY, OFF_STUDY
from edc_constants.constants import ALIVE, DEAD, UNKNOWN, PARTICIPANT

from edc_visit_tracking.constants import MISSED_VISIT, COMPLETED_PROTOCOL_VISIT
from edc_visit_tracking.constants import SCHEDULED, UNSCHEDULED, LOST_VISIT

from edc_constants.constants import NEG, POS, IND

ALIVE_DEAD_UNKNOWN = (
    (ALIVE, 'Alive'),
    (DEAD, 'Dead'),
    (UNKNOWN, 'Unknown'),
)

COOKING_METHOD = (
    ('Gas or electric stove', 'Gas or electric stove'),
    ('Paraffin stove', 'Paraffin stove'),
    ('Wood-burning stove or open fire', 'Wood-burning stove or open fire'),
    ('No regular means of heating', 'No regular means of heating')
)

ETHNICITY = (
    ('Black African', 'Black African'),
    ('Caucasian', 'Caucasian'),
    ('Asian', 'Asian'),
    (OTHER, 'Other, specify')
)

HOUSE_TYPE = (
    ('Formal:Tin-roofed, concrete walls',
     'Formal: Tin-roofed, concrete walls'),
    ('Informal: Mud-walled or thatched', 'Informal: Mud-walled or thatched'),
    ('Mixed formal/informal', 'Mixed formal/informal'),
    ('Shack/Mokhukhu', 'Shack/Mokhukhu')
)

HIGHEST_EDUCATION = (
    ('None', 'None'),
    ('Primary', 'Primary'),
    ('Junior Secondary', 'Junior Secondary'),
    ('Senior Secondary', 'Senior Secondary'),
    ('Tertiary', 'Tertiary')
)

MONEY_EARNED = (
    ('None', 'None'),
    ('<P200 per month / <P47 per week', '<P200 per month / <P47 per week'),
    ('P200-500 per month / P47-116 per week',
     'P200-500 per month / P47-116 per week'),
    ('P501-1000 per month / P117 - 231 per week',
     'P501-1000 per month / P117 - 231 per week'),
    ('P1001-5000 per month / P212 - 1157 per week',
     'P1001-5000 per month / P212 - 1157 per week'),
    ('>P5000 per month / >P1157 per week',
     '>P5000 per month / >P1157 per week'),
    ('Unsure', 'Unsure'),
    (OTHER, 'Other, specify')
)

MONEY_PROVIDER = (
    ('You', 'You'),
    ('Partner/husband', 'Partner/husband'),
    ('Mother', 'Mother'),
    ('Father', 'Father'),
    ('Sister', 'Sister'),
    ('Brother', 'Brother'),
    ('Aunt', 'Aunt'),
    ('Uncle', 'Uncle'),
    ('Grandmother', 'Grandmother'),
    ('Grandfather', 'Grandfather'),
    ('Mother-in-law or Father-in-law', 'Mother-in-law or Father-in-law'),
    ('Friend', 'Friend'),
    ('Work collegues', 'Work collegues'),
    ('Unsure', 'Unsure'),
    (OTHER, 'Other, specify')
)

TOILET_FACILITY = (
    ('Indoor toilet', 'Indoor toilet'),
    ('Private latrine for your house/compound',
     'Private latrine for your house/compound'),
    ('Shared latrine with other compounds',
     'Shared latrine with other compounds'),
    ('No latrine facilities', 'No latrine facilities'),
    (OTHER, 'Other, specify')
)

YES_NO_UNKNOWN = (
    (YES, YES),
    (NO, NO),
    ('Unknown', 'Unknown'),
)

YES_NO_UNCERTAIN = (
    ('0', YES),
    ('1', NO),
    ('2', 'Uncertain'),
)

IMMUNIZATIONS = (
    ('Vitamin_A', 'Vitamin A'),
    ('BCG', 'BCG'),
    ('Hepatitis_B', 'Hepatitis B'),
    ('DPT', 'DPT (Diphtheria, Pertussis and Tetanus)'),
    ('Haemophilus_influenza', 'Haemophilus Influenza B Vaccine'),
    ('PCV_Vaccine', 'PCV Vaccine (Pneumonia Conjugated Vaccine)'),
    ('Polio', 'Polio'),
    ('Rotavirus', 'Rotavirus'),
    ('inactivated_polio_vaccine', 'Inactivated-Polio Vaccine'),
    ('Measles', 'Measles'),
    ('Pentavalent',
     'Pentavalent Vaccine (Contains DPT, Hepatitis B and Haemophilus Influenza B Vaccine)'),
    ('diptheria_tetanus', 'Diptheria and Tetanus')
)

INFANT_AGE_VACCINE_GIVEN = (
    ('At Birth', 'At Birth'),
    ('After Birth', 'After Birth'),
    ('2', '2 months'),
    ('3', '3 months'),
    ('4', '4 months'),
    ('4-6', '4-6 months'),
    ('6-11', '6-11 months'),
    ('9', '9 months'),
    ('9-12', '9-12 months'),
    ('12-17', '12-17 months'),
    ('18', '18 months'),
    ('18-29', '18-29 months'),
    ('24-29', '24-29 months'),
    ('30-35', '30-35 months'),
    ('36-41', '36-41 months'),
    ('42-47', '42-47 months'),
    ('48-53', '48-53 months'),
    ('54-59', '54-59 months')
)

INFO_PROVIDER = (
    ('MOTHER', 'Mother'),
    ('GRANDMOTHER', 'Grandmother'),
    ('FATHER', 'Father'),
    ('GRANDFATHER', 'Grandfather'),
    ('SIBLING', 'Sibling'),
    (OTHER, 'Other'),
)

REASONS_VACCINES_MISSED = (
    ('missed scheduled vaccination', 'Mother or Caregiver has not yet taken infant '
        'to clinic for this scheduled vaccination'),
    ('caregiver declines vaccination',
     'Mother or Caregiver declines this vaccicnation'),
    ('no stock', 'Stock out at clinic'),
    (OTHER, 'Other, specify'),
)

VISIT_INFO_SOURCE = [
    (PARTICIPANT, 'Clinic visit with participant'),
    ('other_contact',
     'Other contact with participant (for example telephone call)'),
    ('other_doctor',
     'Contact with external health care provider/medical doctor'),
    ('family',
     'Contact with family or designated person who can provide information'),
    ('chart', 'Hospital chart or other medical record'),
    (OTHER, 'Other')]

VISIT_REASON = [
    (SCHEDULED, 'Scheduled visit/contact'),
    (MISSED_VISIT, 'Missed Scheduled visit'),
    (UNSCHEDULED,
     'Unscheduled visit at which lab samples or data are being submitted'),
    (LOST_VISIT, 'Lost to follow-up (use only when taking subject off study)'),
    (FAILED_ELIGIBILITY, 'Subject failed enrollment eligibility'),
    (COMPLETED_PROTOCOL_VISIT, 'Subject has completed the study')
]

VISIT_STUDY_STATUS = (
    (ON_STUDY, 'On study'),
    (OFF_STUDY,
     'Off study-no further follow-up (including death); use only '
     'for last study contact'),
)

WATER_SOURCE = (
    ('Piped directly into the house', 'Piped directly into the house'),
    ('Tap in the yard', 'Tap in the yard'),
    ('Communal standpipe', 'Communal standpipe'),
    (OTHER, 'Other water source (stream, borehole, rainwater, etc)')
)

POS_NEG_IND = (
    (POS, 'Positive'),
    (NEG, 'Negative'),
    (IND, 'Indeterminate')
)
