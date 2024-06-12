from django.utils.translation import ugettext_lazy as _
from edc_constants.constants import (ABNORMAL, DONT_KNOW, FAILED_ELIGIBILITY, FEMALE,
                                     MALE,
                                     NO, NORMAL, OFF_STUDY, ON_STUDY, OTHER, YES)
from edc_constants.constants import ALIVE, DEAD, NOT_APPLICABLE, PARTICIPANT, UNKNOWN
from edc_constants.constants import IND, NEG, PENDING, POS
from edc_visit_tracking.constants import COMPLETED_PROTOCOL_VISIT, MISSED_VISIT
from edc_visit_tracking.constants import LOST_VISIT, SCHEDULED, UNSCHEDULED

from .constants import BREASTFEED_ONLY, NOT_RECEIVED, PNTA

HIV_STATUS = (
    (POS, 'Positive'),
    (NEG, 'Negative'),
    (UNKNOWN, 'Unknown')
)

ALIVE_DEAD_UNKNOWN = (
    (ALIVE, 'Alive'),
    (DEAD, 'Dead'),
    (UNKNOWN, 'Unknown'),
)

ANSWERER = (
    ('caregiver', 'Caregiver'),
    ('child_adolescent', 'Child/Adolescent'),
)

BRIEF2_SCALE = (
    ('never', 'Never'),
    ('sometimes', 'Sometimes'),
    ('often', 'Often'),
)

CARDIOVASCULAR_DISORDER = (
    ('None', 'None'),
    ('Truncus arteriosus', 'Truncus arteriosus'),
    ('Atrial septal defect', 'Atrial septal defect'),
    ('Ventricula septal defect', 'Ventricula septal defect'),
    ('Atrioventricular canal', 'Atrioventricular canal'),
    ('Complete transposition of the great vessels (without VSD)',
     'Complete transposition of the great vessels (without VSD)'),
    ('Complete transposition of the great vessels (with VSD)',
     'Complete transposition of the great vessels (with VSD)'),
    ('Tetralogy of Fallot', 'Tetralogy of Fallot'),
    ('Pulmonary valve stenosis or atresia',
     'Pulmonary valve stenosis or atresia'),
    ('Tricuspid valve stenosis or atresia',
     'Tricuspid valve stenosis or atresia'),
    ('Mitral valve stenosis or atresia', 'Mitral valve stenosis or atresia'),
    ('Hypoplastic left ventricle', 'Hypoplastic left ventricle'),
    ('Hypoplastic right ventricle', 'Hypoplastic right ventricle'),
    ('Congenital cardiomyopath (do not code if only isolated cardiomegaly)',
     'Congenital cardiomyopath (do not code if only isolated cardiomegaly)'),
    ('Coarclation of the aorta', 'Coarclation of the aorta'),
    ('Total anomalous pulmonary venous return',
     'Total anomalous pulmonary venous return'),
    ('Arteriovenous malformation, specify site',
     'Arteriovenous malformation, specify site'),
    ('Patent ductous arteriosus (persisting >6 weeks of age)',
     'Patent ductous arteriosus (persisting >6 weeks of age)'),
    (OTHER, 'Other cardiovascular malformation, specify'),
)

CBCL_SCALE = (
    ('not_true', 'Not True (as far you know)'),
    ('somewhat', 'Somewhat or Sometimes True'),
    ('very_true', 'Very True or Often True'),
)

CHILD_AGE_VACCINE_GIVEN = (
    ('at_birth', 'At Birth'),
    ('after_birth', 'After Birth'),
    ('2', '2 months'),
    ('3', '3 months'),
    ('4', '4 months'),
    ('4to6', '4-6 months'),
    ('6to11', '6-11 months'),
    ('9', '9 months'),
    ('9to12', '9-12 months'),
    ('12to17', '12-17 months'),
    ('18', '18 months'),
    ('18to29', '18-29 months'),
    ('24to29', '24-29 months'),
    ('30to35', '30-35 months'),
    ('36to41', '36-41 months'),
    ('42to47', '42-47 months'),
    ('48to53', '48-53 months'),
    ('54to59', '54-59 months'),
    ('adolescent', 'Adolescent Stage'),
    ('catch_up_vaccine', 'Catch-up vaccine')
)

CLEFT_DISORDER = (
    ('None', 'None'),
    ('Cleft lip without cleft palate', 'Cleft lip without cleft palate'),
    ('Cleft palate without cleft lip', 'Cleft palate without cleft lip'),
    ('Cleft lip and palate', 'Cleft lip and palate'),
    ('Cleft uvula', 'Cleft uvula'),
)

CNS_ABNORMALITIES = (
    ('None', 'None'),
    ('Anencephaly', 'Anencephaly'),
    ('Encephaloceis', 'Encephaloceis'),
    ('Spina bifida, open', 'Spina bifida, open'),
    ('Spina bifida, closed', 'Spina bifida, closed'),
    ('Holoprosencephaly', 'Holoprosencephaly'),
    ('Isolated hydroencephaly (not associated with spina bifida)',
     'Isolated hydroencephaly (not associated with spina bifida)'),
    ('Other CNS defect, specify', 'Other CNS defect, specify'),
)

COHORTS = (
    ('cohort_a', 'Cohort A'),
    ('cohort_b', 'Cohort B'),
    ('cohort_c', 'Cohort C'),
    ('cohort_a_sec', 'Cohort A Secondary Aims'),
    ('cohort_b_sec', 'Cohort B Secondary Aims'),
    ('cohort_c_sec', 'Cohort C Secondary Aims'),
    ('cohort_pool', 'Cohort Pool Secondary Aims'),)

COWS_MILK = (
    ('boiled', '1. Boiled from cow'),
    ('unboiled', '2. Unboiled from cow'),
    ('store', '3. From store'),
    (NOT_APPLICABLE, 'Not Applicable'),)

COOKING_METHOD = (
    ('Gas or electric stove', 'Gas or electric stove'),
    ('Paraffin stove', 'Paraffin stove'),
    ('Wood-burning stove or open fire', 'Wood-burning stove or open fire'),
    ('No regular means of heating', 'No regular means of heating')
)

DEPRESSION_SCALE = (
    ('0', 'Not at all'),
    ('1', 'Several days'),
    ('2', 'More than half the days'),
    ('3', 'Nearly every day'),
)

FOOD = (
    ('often_true ', 'Often True'),
    ('sometimes_true ', 'Sometimes True '),
    ('never_true', 'Never True'),
    ('dont_know', 'I don’t know or Refused to answer'),
)

DIFFICULTY_LEVEL = (
    ('not_difficult', 'Not difficult'),
    ('somewhat_difficult', 'Somewhat difficult'),
    ('very_difficult', 'Very difficult'),
    ('extremely_difficult', 'Extremely difficult'),
)

YES_NO_DN_PNTA = (
    (YES, YES),
    (NO, NO),
    ('dont_know', 'I do not know'),
    (PNTA, _('Prefer not to answer')),
)

EMO_SUPPORT_DECLINE = (
    ('not_yet_sought_clinic', 'I have not yet sought the clinic'),
    ('could_not_get_clinic_booking',
     'I went to the clinic but could not get a booking'),
    ('partner_dnw_me_to_attend', 'My partner does not want me to attend'),
    ('family_dnw_me_to_attend', 'My family does not want me to attend'),
    ('no_longer_need_support', 'I felt I no longer need emotional support'),
    ('work_constraints', 'Work constraints'),
    ('no_transport_fare', 'I did not have transport fare'),
    (OTHER, 'Other, specify'),)

EMO_SUPPORT_PROVIDER = (
    ('psychologist', 'Psychologist'),
    ('hosp_social_worker', 'Hospital-based social worker'),
    ('comm_social_worker', 'Community Social worker'),
    ('psychiatrist', 'Psychiatrist'),
    (PNTA, _('Prefer not to answer')),)

NO_EMO_SUPPORT_REASON = (
    ('professional_not_around', 'Social worker/ Psychologist/ Psychiatrist not around'),
    ('clinic_long_queue', 'Long queue at the clinic'),
    ('told_idn_emo_support', 'I was told I don’t need emotional support'),
    ('was_treated_well_at_facility',
     'I was not treated well at the health facility and I had to leave'),
    ('changed_mind', 'Changed mind and returned home'),
    (OTHER, 'Other, specify'),)

PERCEIVE_COUNSELOR = (
    ('approachable', 'Approachable'),
    ('respectful', 'Respectful'),
    ('trustworthy', 'Trustworthy'),
    ('patient', 'Patient'),
    ('demeaning', 'Demeaning'),
    ('judgmental', 'Judgmental'),
    ('discriminatory', 'Discriminatory'),
    (PNTA, _('Prefer not to answer')),
    (OTHER, 'Other, specify'))

ETHNICITY = (
    ('Black African', 'Black African'),
    ('Caucasian', 'Caucasian'),
    ('Asian', 'Asian'),
    (OTHER, 'Other, specify')
)

FACIAL_DEFECT = (
    ('None', 'None'),
    ('Anophthalmia/micro-opthalmia', 'Anophthalmia/micro-opthalmia'),
    ('Cataracts', 'Cataracts'),
    ('Coloboma', 'Coloboma'),
    ('OTHER eye abnormality', 'Other eye abnormality, specify'),
    ('Absence of ear', 'Absence of ear'),
    ('Absence of auditory canal', 'Absence of auditory canal'),
    ('Congenital deafness', 'Congenital deafness'),
    ('Microtia', 'Microtia'),
    ('OTHER ear anomaly', 'Other ear anomaly, specify'),
    ('Brachial cleft cyst, sinus or pit', 'Brachial cleft cyst, sinus or pit'),
    ('OTHER facial malformation', 'Other facial malformation, specify'),
)

FEEDING_CHOICES = (
    (BREASTFEED_ONLY, 'Breastfeed only'),
    ('Formula feeding only', 'Formula feeding only'),
    ('Both breastfeeding and formula feeding',
     'Both breastfeeding and formula feeding'),
    ('Medical complications: Infant did not feed',
     'Medical complications: Infant did not feed'),
)

FEM_GENITAL_ANOMALY = (
    ('None', 'None'),
    ('Ambinguous genitalia, female', 'Ambinguous genitalia, female'),
    ('Vaginal agenesis', 'Vaginal agenesis'),
    ('Absent or streak ovary', 'Absent or streak ovary'),
    ('Uterine anomaly', 'Uterine anomaly'),
    (OTHER,
     'Other ovarian, fallopian, uterine, cervical, vaginal, or vulvar abnormality'),
)

FREQUENCY_BREASTMILK_REC = (
    ('less_than_once_per_week', 'Less than once per week'),
    ('less_than_once_per_day',
     'Less than once per day, but at least once per week'),
    ('once_per_day', 'About once per day on most days'),
    ('more_than_once_per_day',
     'More than once per day, but not for all feedings'),
    ('all_feedings',
     'For all feedings (i.e no formula or other foods or liquids'),
    (NOT_APPLICABLE, 'Not applicable'),
)

GENDER_NA = (
    (MALE, _('Male')),
    (FEMALE, _('Female')),
    (NOT_APPLICABLE, 'Not Applicable'),
)

GRADE_LEVEL = (
    ('standard_1', 'Standard 1'),
    ('standard_2', 'Standard 2'),
)

HIGHEST_EDUCATION = (
    ('pre_school', 'Pre-school'),
    ('standard_1', 'Standard 1'),
    ('standard_2', 'Standard 2'),
    ('standard_3', 'Standard 3'),
    ('standard_4', 'Standard 4'),
    ('standard_5', 'Standard 5'),
    ('standard_6', 'Standard 6'),
    ('standard_7', 'Standard 7'),
    ('form_1', 'Form 1'),
    ('form_2', 'Form 2'),
    ('form_3', 'Form 3'),
    ('form_4', 'Form 4'),
    ('form_5', 'Form 5'),
    ('university', 'Tertiary/University'),
    (OTHER, 'Other'),
    ('no_schooling', 'No Schooling ')
)

HOSPITAL = (
    ('princess_marina', 'Princess Marina'),
    ('slh', 'SLH'),
    ('drmh', 'DRMH'),
    ('tph', 'Thamaga Primary Hospital'),
    ('sda', 'SDA'),
    ('blh', 'BLH'),
    ('athlone ', 'Athlone '),
    (OTHER, 'Other'),
)
HOSPITALISATION_REASON = (
    ('pneumonia', 'Pneumonia'),
    ('tuberculosis', 'Tuberculosis'),
    ('bronchiolitis', 'Bronchiolitis'),
    ('laryngotracheobronchitis', 'Laryngotracheobronchitis/Croup'),
    ('acute', 'Acute diarrheal disease'),
    ('persistent', 'Persistent diarrheal disease'),
    ('meningitis', 'Meningitis'),
    ('malaria', 'Malaria'),
    ('measles', 'Measles'),
    ('trauma', 'Trauma'),
    ('febrile', 'Febrile seizure'),
    ('malnutrition', 'Malnutrition'),
    ('anemia', 'Anemia'),
    ('surgical', 'Surgical reasons'),
    ('other', 'Other'),
)
HOUSE_TYPE = (
    ('Formal:Tin-roofed, concrete walls',
     'Formal: Tin-roofed, concrete walls'),
    ('Informal: Mud-walled or thatched', 'Informal: Mud-walled or thatched'),
    ('Mixed formal/informal', 'Mixed formal/informal'),
    ('Shack/Mokhukhu', 'Shack/Mokhukhu')
)

HOW_OFTEN = (
    ('almost_every_month', 'Almost every month'),
    ('some_months', 'Some months but not every month'),
    ('one_or_two', 'Only 1 or 2 months'),
    ('i_dont_know', 'I don’t know'),
)

IDENTITY_TYPE = (
    ('country_id', 'Country ID number'),
    ('birth_cert', 'Birth Certificate number'),
    ('country_id_rcpt', 'Country ID receipt'),
    ('passport', 'Passport'),
    (OTHER, 'Other'),
)

IMMUNIZATIONS = (
    ('vitamin_a', 'Vitamin A'),
    ('bcg', 'BCG'),
    ('hepatitis_b', 'Hepatitis B'),
    ('dpt', 'DPT (Diphtheria, Pertussis and Tetanus)'),
    ('haemophilus_influenza', 'Haemophilus Influenza B Vaccine'),
    ('pcv_vaccine', 'PCV Vaccine (Pneumonia Conjugated Vaccine)'),
    ('polio', 'Polio'),
    ('rotavirus', 'Rotavirus'),
    ('inactivated_polio_vaccine', 'Inactivated-Polio Vaccine'),
    ('measles', 'Measles'),
    ('pentavalent',
     'Pentavalent Vaccine (Contains DPT, Hepatitis B and Haemophilus Influenza B '
     'Vaccine)'),
    ('diptheria_tetanus', 'Diptheria and Tetanus'),
    ('hpv_vaccine', 'HPV Vaccine'),
    ('measles_rubella', 'Measles and Rubella')
)

INFANT_VACCINATIONS = (
    ('Vitamin_A', 'Vitamin A'),
    ('BCG', 'BCG'),
    ('Hepatitis_B', 'Hepatitis B'),
    ('DPT', 'DPT (Diphtheria, Pertussis and Tetanus)'),
    ('Haemophilus_influenza', 'Haemophilus Influenza B Vaccine'),
    ('PCV_Vaccine', 'PCV Vaccine (Pneumonia Conjugated Vaccine)'),
    ('Polio', 'Polio'),
    ('inactivated_polio_vaccine', 'Inactivated-Polio Vaccine'),
    ('Rotavirus', 'Rotavirus'),
    ('Measles', 'Measles'),
    ('Pentavalent',
     'Pentavalent Vaccine (Contains DPT, Hepatitis B and Haemophilus Influenza B '
     'Vaccine)'),
    ('diphtheria_tetanus', 'Diphtheria and Tetanus')
)

INFO_PROVIDER = (
    ('MOTHER', 'Mother'),
    ('GRANDMOTHER', 'Grandmother'),
    ('FATHER', 'Father'),
    ('GRANDFATHER', 'Grandfather'),
    ('SIBLING', 'Sibling'),
    ('self', 'Self'),
    (OTHER, 'Other'),
)

IS_DATE_ESTIMATED = (
    (NO, 'No'),
    ('Yes, estimated the Day', 'Yes, estimated the Day'),
    ('Yes, estimated Month and Day', 'Yes, estimated Month and Day'),
    ('Yes, estimated Year, Month and Day',
     'Yes, estimated Year, Month and Day'),
)

KNOW_HIV_STATUS = (
    ('Nobody', 'Nobody'),
    ('1 person', '1 person'),
    ('2-5 people', '2-5 people'),
    ('6-10 people', '6-10 people'),
    ('More than 10 people', 'More than 10 people'),
    ('dont know', 'I do not know'),)

LOWEST_CD4_KNOWN = (
    (YES, 'Yes'),
    (NO, 'No'),
    (NOT_APPLICABLE, 'Not applicable')
)

LOWER_GASTROINTESTINAL_ABNORMALITY = (
    ('None', 'None'),
    ('Duodenal atresia, stenosis, or absence',
     'Duodenal atresia, stenosis, or absence'),
    ('Jejunal atresis, stenosis, or absence',
     'Jejunal atresis, stenosis, or absence'),
    ('Ileal atresia, stenosis, or absence',
     'Ileal atresia, stenosis, or absence'),
    ('Atresia, stenosis, or absence of large intestine, rectum, or anus',
     'Atresia, stenosis, or absence of large intestine, rectum, or anus'),
    ('Hirschsprung disease', 'Hirschsprung disease'),
    ('OTHER megacolon', 'Other megacolon'),
    ('Liver, pancreas, or gall bladder defect, specify',
     'Liver, pancreas, or gall bladder defect, specify'),
    ('Diaphramtic hernia', 'Diaphramtic hernia'),
    ('OTHER GI anomaly', 'Other GI anomaly, specify'),
)

MALE_GENITAL_ANOMALY = (
    ('None', 'None'),
    ('Hypospadias, specify degree', 'Hypospadias, specify degree'),
    ('Chordee', 'Chordee'),
    ('Ambiguous genitalia, male', 'Ambiguous genitalia, male'),
    ('Undescended testis', 'Undescended testis'),
    (OTHER, 'Other male genital abnormality, specify'),
)

MARKS = (
    ('a', 'A'),
    ('b', 'B'),
    ('c', 'C'),
    ('d', 'D'),
    ('e', 'E'),
    ('f', 'F'),
    ('g', 'G'),
    ('u', 'U'),
    ('pending', 'Pending'),
    ('not_taking_subject', 'Not taking subject'),
    ('never_sat_for_exam', 'Never sat for subject examination'),
    ('I_do_not_know_right_now', 'I do not know right now'),
)

MENARCHE_AVAIL = (
    (YES, YES),
    (NO, NO),
    ('not_reached', 'Not reached menarche'),
    (NOT_APPLICABLE, 'Not Applicable')
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

MOUTH_UP_GASTROINT_DISORDER = (
    ('None', 'None'),
    ('Aglossia', 'Aglossia'),
    ('Macroglossia', 'Macroglossia'),
    ('OTHER mouth, lip, or tongue',
     'Other mouth, lip, or tongue anomaly, specify'),
    ('Esophageal atresia', 'Esophageal atresia'),
    ('Tracheoesphageal fistula', 'Tracheoesphageal fistula'),
    ('Esophageal web', 'Esophageal web'),
    ('Pyloric stenosis', 'Pyloric stenosis'),
    ('OTHER esophageal or stomach',
     'Other esophageal or stomach abnormality, specify'),
)

MUSCULOSKELETAL_ABNORMALITY = (
    ('None', 'None'),
    ('Craniosynostosis', 'Craniosynostosis'),
    ('Torticollis', 'Torticollis'),
    ('Congenital scoliosis, lordosis', 'Congenital scoliosis, lordosis'),
    ('Congenital dislocation of hip', 'Congenital dislocation of hip'),
    ('Talipes equinovarus (club feet excluding metatarsus varus)',
     'Talipes equinovarus (club feet excluding metatarsus varus)'),
    ('Funnel chest or pigeon chest (pectus excavatum or carinaturn)',
     'Funnel chest or pigeon chest (pectus excavatum or carinaturn)'),
    ('Polydactyly', 'Polydactyly'),
    ('Syndactyly', 'Syndactyly'),
    ('Other hand malformation, specify', 'Other hand malformation, specify'),
    ('Webbed fingers or toes', 'Webbed fingers or toes'),
    ('Upper limb reduction defect, specify',
     'Upper limb reduction defect, specify'),
    ('Lower limb reduction defect, specify',
     'Lower limb reduction defect, specify'),
    ('Other limb defect, specify', 'Other limb defect, specify'),
    ('Other skull abnormality, specify', 'Other skull abnormality, specify'),
    ('Anthrogryposis', 'Anthrogryposis'),
    ('Vertebral or rib abnormalities, specify',
     'Vertebral or rib abnormalities, specify'),
    ('Osteogenesis imperfecta', 'Osteogenesis imperfecta'),
    ('Dwarfing syndrome, specify', 'Dwarfing syndrome, specify'),
    ('Congenital diaphramatic hernia', 'Congenital diaphramatic hernia'),
    ('Omphalocele', 'Omphalocele'),
    ('Gastroschisis', 'Gastroschisis'),
    (OTHER, 'Other muscular or skeletal abnormality or syndrome, specify'),
)

NUMBER_OF_DAYS = (
    ('one', '1'),
    ('two', '2'),
    ('three', '3'),
    ('four', '4'),
    ('five', '5'),
)

OTHER_DEFECT = (
    ('None', 'None'),
    (OTHER, 'Other defect/syndrome not already reported, specify'),
)

OVERALL_MARKS = (
    ('a', 'A'),
    ('b', 'B'),
    ('c', 'C'),
    ('d', 'D'),
    ('e', 'E'),
    ('f', 'F'),
    ('g', 'G'),
    ('u', 'U'),
    ('points', 'Points'),
    ('pending', 'Pending'),
    ('never_sat', 'Never sat for subject examination'),
    ('I_do_not_know_right_now', 'I do not know right now'),
)

OP_TYPE = (
    ('new_illness', 'New illness'),
    ('growth_check', 'Growth check'),
    ('immunizations', 'Immunizations'),
    ('mental_health', 'Mental Health'),
    (UNKNOWN, 'Unknown'),
    (OTHER, 'Other, specify'),
)

PENNCNB_INVALID = (
    ('no_impact', 'No Impact'),
    ('child_ill', 'Child was ill'),
    ('sensory_handicap', 'Child has a sensory handicap'),
    ('motor_handicap', 'Child has a motor handicap'),
    ('uncooperative', 'Child was uncooperative'),
    ('misunderstood_instructions', 'Child did not understand instructions'),
    ('unavailable_resources', 'Equipment/room was not available'),
    (OTHER, 'Other, specify'),
)

PHYS_ACTIVITY_TIME = (
    ('specify_hrs_mins', 'Hours and minutes per day (specify)'),
    (DONT_KNOW, 'Don\'t know/Not sure')
)

POS_NEG_IND = (
    (POS, 'Positive'),
    (NEG, 'Negative'),
    (IND, 'Indeterminate')
)

POS_NEG_IND_INVALID = (
    (POS, 'Positive'),
    (NEG, 'Negative'),
    (IND, 'Indeterminate'),
    ('invalid', 'Invalid')
)

REASONS_PENNCNB_INCOMPLETE = (
    ('software_errors', 'Software/Application errors'),
    ('restless_child', 'Child was restless'),
    ('lack_of_understanding', 'Child could not understand the program'),
    ('no_private_space', 'No private space/room available for test'),
    ('handicapped', 'Child is handicapped (please provide additional information in Q9)'),
    (OTHER, 'Other, specify'),
)

REASONS_VACCINES_MISSED = (
    ('missed_sched_vaccine', 'Mother or Caregiver has not yet taken infant '
                             'to clinic for this scheduled vaccination'),
    ('caregiver_declines_vaccination',
     'Mother or Caregiver declines this vaccicnation'),
    ('no_stock', 'Stock out at clinic'),
    (OTHER, 'Other, specify'),
)

REFERRED_TO = (
    ('community_social_worker', 'Community Social Worker'),
    ('hospital_based_social_worker', 'Hospital-based Social Worker'),
    ('a&e', 'A&E'),
    ('psychologist', 'Psychologist'),
    ('psychiatrist', 'Psychiatrist'),
    ('receiving_emotional_care', 'Already receiving emotional care'),
    ('declined', 'Declined'),
    (OTHER, 'Other'),
)

RENAL_ANOMALY = (
    ('None', 'None'),
    ('Bilateral renal agenesis', 'Bilateral renal agenesis'),
    ('Unilateral renal agenesis or dysplasia',
     'Unilateral renal agenesis or dysplasia'),
    ('Polycystic kidneys', 'Polycystic kidneys'),
    ('Congenital hydronephrosis', 'Congenital hydronephrosis'),
    ('Unilateral stricture, stenosis, or hypoplasia',
     'Unilateral stricture, stenosis, or hypoplasia'),
    ('Duplicated kidney or collecting system',
     'Duplicated kidney or collecting system'),
    ('Horseshoe kidney', 'Horseshoe kidney'),
    ('Exstrophy of bladder', 'Exstrophy of bladder'),
    ('Posterior urethral valves', 'Posterior urethral valves'),
    (OTHER, 'Other renal, ureteral, bladder, urethral abnormality, specify'),
)

RESPIRATORY_DEFECT = (
    ('None', 'None'),
    ('Choanal atresia', 'Choanal atresia'),
    ('Agenesis or underdevelopment of nose',
     'Agenesis or underdevelopment of nose'),
    ('Nasal cleft', 'Nasal cleft'),
    ('Single nostril, proboscis', 'Single nostril, proboscis'),
    ('OTHER nasal or sinus abnormality',
     'Other nasal or sinus abnormality, specify'),
    ('Lryngeal web. glottic or subglottic',
     'Lryngeal web. glottic or subglottic'),
    ('Congenital laryngeal stenosis', 'Congenital laryngeal stenosis'),
    ('OTHER laryngeal, tracheal or bronchial anomalies',
     'Other laryngeal, tracheal or bronchial anomalies'),
    ('Single lung cyst', 'Single lung cyst'),
    ('Polycystic lung', 'Polycystic lung'),
    (OTHER, 'Other respiratory anomaly, specify'),
)

SCHOOL_TYPE = (
    ('public', 'Public/Government'),
    ('private', 'Private'),
    ('public_boarding_school', 'Boarding School Public/Government'),
    ('private_boarding_school', 'Boarding School Private'),
    (NOT_APPLICABLE, 'Not applicable'),
)

SKIN_ABNORMALITY = (
    ('None', 'None'),
    ('Icthyosis', 'Icthyosis'),
    ('Ectodermal dysplasia', 'Ectodermal dysplasia'),
    (OTHER, 'Other skin abnormality, specify'),
)

TANNER_STAGES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    (NOT_APPLICABLE, 'Not Applicable'),
)

TIMES_BREASTFED = (
    ('<1 per week', '1. Less than once per week'),
    ('<1 per day, but at least once per week',
     '2. Less than once per day, but at least once per week'),
    ('about 1 per day on most days', '3. About once per day on most days'),
    ('>1 per day, but not for all feedings',
     '4. More than once per day, but not for all feedings'),
    ('For all feedings',
     '5. For all feedings (i.e no formula or other foods or liquids)'),
    (NOT_APPLICABLE, 'Not Applicable'),
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

TRISOME_CHROSOMESOME_ABNORMALITY = (
    ('None', 'None'),
    ('Trisomy 21', 'Trisomy 21'),
    ('Trisomy 13', 'Trisomy 13'),
    ('Trisomy 18', 'Trisomy 18'),
    ('OTHER trisomy, specify', 'Other trisomy, specify'),
    ('OTHER non-trisomic chromosome',
     'Other non-trisomic chromosome abnormality, specify'),
)

UNCERTAIN_GEST_AGE = (
    ('born_on_time', 'This child was born on time'),
    ('born_early', 'This child was born early'),
    ('born_late', 'This child was born late'),
    ('unknown', 'This child’s gestational age is unknown')
)

VIGOROUS_ACTIVITY_DAYS = (
    ('days_per_week', 'Days per week (specify)'),
    ('no_vig_activity', 'No vigorous physical activities')
)

MODERATE_ACTIVITY_DAYS = (
    ('days_per_week', 'Days per week (specify)'),
    ('no_mod_activity', 'No moderate physical activities')
)

WALKING_DAYS = (
    ('days_per_week', 'Days per week (specify)'),
    ('no_walking', 'No walking')
)

WORK_TYPE = (
    ('construction', 'Construction'),
    ('retail', 'Retail'),
    ('domestic', 'Domestic'),
    ('security', 'Security'),
    ('hospitality', 'Hospitality'),
    ('tirelo_sechaba', 'Tirelo Sechaba (volunteers)'),
    (OTHER, 'Other, specify')
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

WATER_USED = (
    ('Water direct from source', 'Water direct from source'),
    ('Water boiled immediately before use',
     'Water boiled immediately before use'),
    ('Water boiled earlier and then stored',
     'Water boiled earlier and then stored'),
    ('Water not required', 'Water not required (ready-made or pre-made formula milk)'),
    ('Specifically treated water', 'Specifically treated water'),
    (OTHER, 'Other (specify)'),
    (NOT_APPLICABLE, 'Not Applicable'),
)

YES_NO_DONT_KNOW = (
    (YES, YES),
    (NO, NO),
    ('i_dont_know', 'I don’t know')
)

YES_NO_UNKNOWN = (
    (YES, YES),
    (NO, NO),
    (UNKNOWN, 'Unknown'),
)

YES_NO_UNKNOWN_NA = (
    (YES, YES),
    (NO, NO),
    (UNKNOWN, 'Unknown'),
    (NOT_APPLICABLE, 'Not applicable'),
)

YES_NO_UNCERTAIN = (
    ('0', NO),
    ('1', YES),
    ('2', 'Uncertain'),
)

YES_NO_NOT_ASKED = (
    (YES, YES),
    (NO, NO),
    ('did_not_ask_child', 'Did not ask the child/adolescent'),
)

BF_ESTIMATED = (
    ('gen_est', 'Yes - General estimation'),
    ('used_infant_dob', 'Yes - Used infant date of birth'),
    (NO, NO)
)

'''
Choices for the covid form
'''

YES_NO_COVID_FORM = (
    (YES, 'Yes'),
    (NO, 'No'),
    ('tried_but_could_not_get_tested', 'Tried, but could not get tested '),
    (UNKNOWN, 'Unknown'),

)

TESTING_REASONS = (
    ('pre-traveling_screening ', 'Pre-Traveling screening'),
    ('routine_testing ', 'Routine testing (experiencing symptoms)'),
    ('contact_tracing', 'Contact tracing'),
    ('asymptomatic_testing', 'Routine Testing(Asymptomatic)'),
    (OTHER, 'Other')
)

POS_NEG_PENDING_UNKNOWN = (
    (POS, 'Positive'),
    (NEG, 'Negative'),
    (PENDING, 'Pending'),
    (IND, 'Indeterminate'),
    (UNKNOWN, 'Unknown'),
)

POS_NEG_PENDING_NOT_RECEIVED = (
    (POS, 'Positive'),
    (NEG, 'Negative'),
    (PENDING, 'Pending'),
    (NOT_RECEIVED, 'Not Received'),
)

ISOLATION_LOCATION = (
    ('home', 'Home'),
    ('hospital', 'Hospital'),
    ('clinic', 'Clinic'),
    (OTHER, 'Other'),
)

YES_NO_PARTIALLY = (
    (YES, 'Yes'),
    (NO, 'No'),
    ('partially_jab', 'Partially'),

)

VACCINATION_TYPE = (
    ('astrazeneca', 'AstraZeneca'),
    ('sinovac', 'Sinovac'),
    ('pfizer', 'Pfizer'),
    ('johnson_and_johnson', 'Johnson & Johnson '),
    ('moderna', 'Moderna'),
    (OTHER, 'Other')
)
HEARING_SPECIALISTS = (
    ('no_referral', 'No Referral'),
    ('speech_therapy', 'Speech Therapy'),
    ('audiology', 'Audiology'),
    ('doctor', 'Doctor'),
)

VISION_SPECIALISTS = (
    ('no_referral', 'No Referral'),
    ('optometrist', 'Optometrist'),
    ('ophthalmic_nurse', 'Ophthalmic nurse'),
    ('occupational_therapist', 'Occupational Therapist'),
    ('doctor', 'Doctor'),
)

COGNITIVE_SPECIALIST = (
    ('no_referral', 'No Referral'),
    ('psychologist', 'Psychologist'),
    ('speech_therapy', 'Speech Therapy'),
    ('occupational_therapist', 'Occupational Therapist'),
    ('doctor', 'Doctor'),
)

MOTOR_SKILLS_SPECIALIST = (
    ('no_referral', 'No Referral'),
    ('physiotherapist', 'Physiotherapist'),
    ('occupational_therapist', 'Occupational Therapist'),
    ('doctor', 'Doctor'),
)

STUDY_SITES = (
    ('40', 'Gaborone'),
)

REASON_NOT_DRAWN = (
    ('collection_failed', 'Tried, but unable to obtain sample from patient'),
    ('absent', 'Patient did not attend visit'),
    ('refused', 'Patient refused'),
    ('no_supplies', 'No supplies'),
    (OTHER, 'Other'),
    (NOT_APPLICABLE, 'Not Applicable'))

YES_NO_NA = (
    (YES, YES),
    (NO, NO),
    (NOT_APPLICABLE, 'Not applicable'),
)

YES_NO_PNTA = (
    (YES, YES),
    (NO, NO),
    (PNTA, _('Prefer not to answer')),
)

COMMUNITY_IMPACT = (
    ('not_a_problem', 'Not a problem'),
    ('a_little_of_a_problem', 'A little bit of a problem'),
    ('neither_little_or_big_problem', 'It is not a little problem nor a big problem'),
    ('somehat_of_a_problem', 'Somewhat of a problem'),
    ('a_big_problem', 'A big problem'),
    (UNKNOWN, 'I do not know'),
    (PNTA, 'Prefer to not answer')
)

COMMUNITY_TREATMENT = (
    ('treated_well', 'Treated well'),
    ('treated_normally', 'Treated normally'),
    ('treated_poorly', 'Treated poorly'),
    (UNKNOWN, 'I do not know'),
    (OTHER, 'Other'),
)

VISIT_NUMBER = (
    ('0', '0'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6_or_more', '6 or more')
)

HEALTH_CARE_CENTER = (
    ('government_health_center', 'Government health center'),
    ('private_clinic', 'Private clinic'),
    ('both', 'Both government health center and private clinic'),
    ('hospital', 'Hospital'),
    ('school_health_clinic', 'school health clinic'),
    (OTHER, 'Other')
)

TB_SYMPTOM = (
    ('respitory_illness', 'Respiratory illness (cough, runny nose, sore throat, etc)'),
    ('gastrointestinal_illness', 'Gastrointestinal illness (vomiting, diarrhea, etc)'),
    ('febrile_illness', 'Febrile illness (with fever)'),
    ('sexual_reporductive_healthy_needs',
     'Sexual reproductive health needs (contraceptives))'),
    (OTHER, 'Other')
)

YES_NO_UNK_PNTA = (
    (YES, YES),
    (NO, NO),
    (UNKNOWN, 'I do not know'),
    (PNTA, 'Prefer not to answer'),)

EXTRA_PULMONARY_LOC = (
    ('lymph_nodes', 'Lymph nodes'),
    ('abdomen', 'Abdomen '),
    ('bones', 'Bones '),
    ('brain', 'Brain'),
    (UNKNOWN, 'Unknown'),
    (OTHER, 'Other')
)

TB_DRUGS_FREQ = (
    ('4_drugs', '4 drugs'),
    ('more_than_4', 'More than 4 drugs'),
    (UNKNOWN, 'Unknown'),
    (PNTA, 'Prefer not to answer'),
)

TB_TYPE = (
    ('inside_the_lungs', 'In the lungs'),
    ('outside_the_lungs', 'Outside the lungs'),
    ('both', 'Both in the lungs and outside the lungs'),
    (UNKNOWN, 'Unknown'),
    (PNTA, 'Prefer not to answer')
)

RELATION_TO_INDIVIDUAL = (
    ('partner', 'Partner'),
    ('child', 'Child'),
    ('mother', 'Mother'),
    ('father', 'Father'),
    ('sibling', 'Sibling'),
    (OTHER, 'Other'),
)

TB_THERAPY_REASONS = (
    (POS, 'Positive test for TB Infection'),
    ('tb_contact', 'TB Contact'),
    ('hiv_positive', 'Diagnosed with HIV'),
    (UNKNOWN, 'Unknown'),
    (OTHER, 'Other'),
)

TB_PRESCRIPTION_AGE = (
    ('0_4', '0-4 years'),
    ('5_9', '5-9 years'),
    ('10_17', '10-17 years')
)

TIMES_TESTED = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('more', 'More'),
)

POS_NEG_IND_IDK = (
    (POS, 'Positive'),
    (NEG, 'Negative'),
    (IND, 'Indeterminate'),
    (UNKNOWN, 'I do not know'),
)

LOCATION_REFERRAL = (
    ('bontleng', 'Bontleng'),
    ('julia_molefe', 'Julia Molefe'),
    ('phase_2', 'Phase 2'),
    ('bh1', 'BH1'),
    ('bh2', 'BH2'),
    ('bh3', 'BH3'),
    ('nkoyaphiri', 'Nokoyaphiri'),
    ('mogoditshane', 'Mogoditshane'),
    ('lesirane', 'Lesirane'),
    ('old_naledi', 'Old Naledi'),
    ('g_west', 'G-West'),
    ('sebele', 'Sebele'),
    (OTHER, 'Other')
)

TB_DIAGONISTIC_TYPE = (
    ('sputum_sample', 'Sputum Sample'),
    ('chest_xray', 'Chest Xray'),
    ('gene_xpert', 'Gene Xpert'),
    ('tst', 'TST'),
    (None, 'None'),
    (OTHER, 'Other')
)

YES_NO_PENDING_UNK = (
    (YES, 'Yes'),
    (NO, 'No'),
    (PENDING, 'Pending'),
    (UNKNOWN, 'Unknown'),
)

INTERVIEW_LOCATIONS = (
    ('FLOURISH_clinic', 'FLOURISH clinic'),
    ('BHP_site', 'BHP site'),
    ('part_home', 'Participant home'),
    (OTHER, 'Other'))

INTERVIEW_LANGUAGE = (
    ('setswana', 'Setswana'),
    ('english', 'English'),
    ('both', 'Both'))

EVAL_LOCATION = (
    ('bontleng', 'Bontleng'),
    ('julia_molefe', 'Julia Molefe'),
    ('phase_2', 'Phase 2'),
    ('BH1', 'BH1'),
    ('BH2', 'BH2'),
    ('BH3', 'BH3'),
    ('nkoyaphiri', 'Nkoyaphiri'),
    ('lesirane', 'Lesirane'),
    ('mogoditshane', 'Mogoditshane'),
    ('old_naledi', 'Old Naledi'),
    ('g_west', 'G-West'),
    ('sebele', 'Sebele'),
    (OTHER, 'Other, specify')
)

YES_NO_UNABLE_DET = (
    (YES, YES),
    (NO, NO),
    (PENDING, 'Pending'),
    ('unable_to_determine', 'Unable to determine'),)

DECLINE_REASON = (
    ('cant_physically_attend', 'Not able to physically come to clinic'),
    ('not_interested', 'Not interested in participating'),
    (OTHER, 'Other (Specify)'),)

YES_NO_NOT_ELIGIBLE = (
    (YES, YES),
    (NO, NO),
    ('not_eligible', 'Not eligible'),)
YES_NO_NOT_COMPLETED = (
    (YES, YES),
    (NO, NO),
    ('start_not_complete', 'Started, but did not complete'),)

CLINIC_NON_VISIT_REASONS = (
    ('out_of_study_area', 'Temporarily out of study area'),
    ('no_fares', 'Participant does not have transport fares'),
    ('school_exams', 'Unable to attend due to school, exams or tests'),
    ('emergency_issues', 'Participant/caregiver has work/home emergency issues'),
    ('work_release', 'Participant/caregiver cannot be released from work'),
    ('isolation', 'Participant is in isolation due to COVID-19 or another infection'),
    ('caregiver_not_well', 'Participant/caregiver is not well'),
    (OTHER, 'Other'),
)

XRAY_RESULTS = (
    (NORMAL, 'Normal'),
    (ABNORMAL, 'Abnormal'),
    (PENDING, 'Pending'),
    (NOT_RECEIVED, 'Not Received')
)

NOT_TESTED_REASON = (
    ('no_apparent_reason', 'No apparent reason'),
    ('missed_visit', 'Missed clinic visit due to time constraints/ No transport fare'),
    ('hcw_decision', 'Healthcare worker did not say it was necessary'),
    ('no_kits', 'Test kits out of stock'),
    (OTHER, 'Other'),
)

PREFERRED_CLINIC = (
    ('local', 'Local Clinic'),
    ('flourish', 'FLOURISH Clinic'),
    ('no_testing', 'I do not wish to have my infant tested at this time'),
    (NOT_APPLICABLE, 'Not Applicable, because under Botswana Guidelines, not currently '
                     'due for testing '),
    (OTHER, 'Other'),
)

CBCL_INTEREST = (
    ('interested', 'Interested and/or cooperative'),
    ('disinterested', 'Disinterested, disliked process'),
    ('unknown', 'Unknown'),
)

CBCL_UNDERSTANDING = (
    ('understood', 'Understood easily'),
    ('mild_difficulty', 'Had mild difficulty understanding'),
    ('significant_difficulty', 'Had significant difficulty understanding'),
    ('unknown', 'Unknown'),
)

CBCL_INVALID_REASON = (
    ('did_not_understand', 'Did not understand the questions'),
    ('uncomfortable_sharing', 'Did not feel comfortable sharing information'),
    ('unknown', 'Unknown'),
    (OTHER, 'Other'),
)

CBCL_IMPACT = (
    ('no_impact', 'No Impact'),
    ('sensory_handicap', 'Child has a sensory handicap'),
    ('motor_handicap', 'Child has a motor handicap'),
    (OTHER, 'Other'),
)

DELIVERY_LOCATION = [
    ('pmh', 'PMH'),
    ('gwest', 'GWest'),
    ('lesirane', 'Lesirane'),
    ('bh3', 'BH3'),
    ('mafitlha_kgosi', 'Mafitlha Kgosi'),
    ('old_naledi', 'Old Naledi'),
    ('drm_hospital', 'DRM Hospital'),
    ('slh', 'SLH'),
    ('blh', 'BLH'),
    ('thamaga_hospital', 'Thamaga Hospital'),
    ('athlone_hospital', 'Athlone Hospital'),
    ('kanye_sda_hospital', 'Kanye SDA Hospital'),
    (OTHER, 'Other'),
    (UNKNOWN, 'Unknown'),
]

DELIVERY_METHOD = [
    ('vaginal', 'Vaginal'),
    ('c_section', 'C-section'),
    (UNKNOWN, 'Unknown'),
]

GESTATIONAL_AGE_KNOWN = [
    ('yes_weeks', 'Yes (in weeks)'),
    ('yes_months', 'Yes (in months)'),
    ('no', 'No')
]

BORN = [
    ('early', 'Early/Pre-term'),
    ('on_time', 'On-time'),
    ('late', 'Late'),
    (UNKNOWN, 'Unknown'),
]

CHILD_TYPE = [
    ('singleton', 'Singleton'),
    ('twin', 'Twin'),
    ('triplet', 'Triplet')
]

YES_NO_DOESNT_WORK_NA = (
    (YES, YES),
    (NO, NO),
    ('Doesnt_work', 'Doesn\'t work'),
    (NOT_APPLICABLE, 'Not Applicable'),
)

NO_ART_REASON = (
    ('lack_of_understanding',
     'Mother did not understand medication instructions and did not collect'),
    ('forgot_meds', 'Mother forget to collect medication'),
    ('out_of_stock', 'Medication was out of stock'),
    ('period_elapsed',
     '72hrs period to start prophylactic antiretroviral medication elapsed'),
    ('didnt_give_baby', 'Medication collected and did not give the baby'),
    (OTHER, 'Other, specify'),
)

ART_PROPH_STATUS = (
    ('in_progress', 'In progress, still taking prophylaxis'),
    ('completed_in_time',
     'Completed PMTCT intervention within stipulated prophylaxis time (28 days)'),
    ('completed_gt_28days',
     'Completed PMTCT intervention with prophylaxis greater than 28 days'),
    ('incomplete',
     'Incomplete, did not finish within stipulated prophylaxis time'),
)

REASON_MODIFIED = (
    ('toxicity_resolved', 'Toxicity decreased/resolved'),
    ('dose_increase', 'Scheduled dose increase'),
    ('triple_art_na', 'Triple ARTs not available'),
    ('anemia', 'Anemia'),
    ('bleeding', 'Bleeding'),
    ('side_effects', 'Side effects'),
    ('toxicity', 'Toxicity'),
    (OTHER, 'Other, specify'),
)

CHILD_ARV_PROPH = (
    ('arv_proph_nvp', 'NVP'),
    ('arv_proph_azt', 'AZT'),
    ('arv_proph_3tc', '3TC'),
    ('arv_proph_ftc', 'FTC'),
    ('arv_proph_alu', 'ALU'),
    ('arv_proph_trv', 'TRV'),
    ('arv_proph_tdf', 'TDF'),
    ('arv_proph_abc', 'ABC'),
    ('arv_proph_ral', 'RAL'),
    (UNKNOWN, 'Unknown'),
)

LAPTOP_CHOICES = (
    ("computer1", "Computer 1 (Serial # FVFHN3S2Q6L4)"),
    ("computer2", "Computer 2 (Serial # FVHHR2JHQ6L4)"),
    ("computer3", "Computer 3 (Serial # CO2HXOZUQ6L4)")
)

CURRENT_MEDICATIONS = (
    ('inhaler', 'Inhaler/Albuterol'),
    ('antibiotics', 'Antibiotics'),
    ('anti_anxiety_drugs', 'Anti-anxiety drugs'),
    ('anti_asthmatic_drugs', 'Anti-asthmatic drugs'),
    ('antidepressant_drugs', 'Antidepressant drugs'),
    ('cholesterol_medications', 'Cholesterol medications'),
    ('diabetic_medications', 'Diabetic medications'),
    ('heart_disease_medications', 'Heart disease medications'),
    ('hypertensive_medications', 'Hypertensive medications'),
    ('pain_killers', 'Pain killers'),
    ('tb_treatment', 'TB Treatment'),
    ('tpt', 'TPT (TB preventive therapy)'),
    ('traditional_medications', 'Traditional medications'),
    ('vitamin_d_supplement', 'Vitamin D supplement'),
    (OTHER, 'Other'),
)

DURATION_MEDICATIONS = (
    ('less_than_week', 'Less than 1 week'),
    ('week_to_2weeks', '1 week to 2 weeks'),
    ('2weeks_to_1month', '2 weeks to 1 month'),
    ('1month_6months', '1 month- 6 months'),
    ('more_than_6months', 'More than 6 months'),
)

CURRENT_SYMPTOMS = (
    ('cough', 'Cough'),
    ('fever', 'Fever'),
    ('headache', 'Headache'),
    ('vomiting', 'Vomiting'),
    ('diarrhea', 'Diarrhea'),
    ('fatigue', 'Fatigue'),
    ('congestion', 'Congestion'),
    ('enlarged_lymph_nodes', 'Enlarged Lymph nodes'),
    (OTHER, 'Other'),
)

CLINIC_VISIT = (
    (YES, YES),
    (NO, NO),
    ('appointment_scheduled', 'Appointment Scheduled'),
    ('will_seek_care', 'Will seek care'),
)

ARV_DRUG_LIST = (
    ('3tc', 'Lamivudine (3TC)'),
    ('ral', 'Raltegravir (RAL)'),
    (OTHER, 'Other, specify'),
)

TB_TEST_CHOICES = (
    ('chest_xray', 'Chest Xray'),
    ('sputum_sample', 'Sputum sample'),
    ('stool_sample', 'Stool sample'),
    ('urine_test', 'Urine test (LAM)'),
    ('skin_test', 'Skin test (TST/Mantoux)'),
    ('blood_test', 'Blood test (quantiferon)'),
    (OTHER, 'Other'),
    ('None', 'None')
)

TEST_RESULTS_CHOICES = (
    (POS, 'positive'),
    (NEG, 'negative'),
    (PENDING, 'pending'),
    (NOT_RECEIVED, 'not_received')
)

DURATION_OPTIONS = (
    ('< 2 weeks', '< 2 weeks'),
    ('>= 2 weeks', '≥ 2 weeks')
)

TB_TREATMENT_CHOICES = (
    (YES, 'Yes'),
    (NO, 'No'),
    ('awaiting_results', 'awaiting_results'),
    (OTHER, 'Other, specify'),
)

YES_NO_OTHER = (
    (YES, _(YES)),
    (NO, _(NO)),
    (OTHER, 'Other, specify'),
)

YES_NO_DN_RECALL = (
    (YES, YES),
    (NO, NO),
    ('do_not_recall', 'Do not recall'),
)

PERIOD_HAPPENED = (
    ('past_6_months', 'Past 6 months'),
    ('more_than_6_months', 'Longer than 6 months ago')
)

HAPPENED = (
    ('never_happened', 'Never Happened'),
    ('ever_happened', 'Ever Happened'),
)
HAPPENED_APP = (
    ('never_happened', 'Never Happened'),
    ('ever_happened', 'Ever Happened'),
    (NOT_APPLICABLE, 'Not Applicable')
)

PERIOD_HAPPENED_DONT_KNOW = (
    ('past_6_months', 'Past 6 months'),
    ('more_than_6_months', 'Longer than 6 months ago'),
    (DONT_KNOW, "Don't know")
)

HAPPENED_DONT_KNOW = (
    ('never_happened', 'Never Happened'),
    ('ever_happened', 'Ever Happened'),
    (DONT_KNOW, "Don't know")
)

HIV_PERSPECTIVE = (
    ('no_one_thinks_that', 'No one thinks that'),
    ('a_few_people_think_that', 'A few people think that'),
    ('most_people_think_that', 'Most people think that'),
    (NOT_APPLICABLE, 'Not Applicable')
)

TB_REFERRAL_REASON_CHOICES = (
    ('cough', 'Cough'),
    ('fever', 'Fever'),
    ('night_sweats', 'Night sweats'),
    ('weight_loss', 'Weight loss'),
    ('fatigue', 'Fatigue'),
    ('household_Contact_with_TB', 'Household Contact with TB'),
    (OTHER, 'Other'),
)

CARETAKERS = [
    ('bio_mother', 'Biological Mother'),
    ('caregiver', 'Caregiver'),
    ('bio_father', 'Biological Father'),
    ('grandmother', 'Grandmother'),
    ('grandfather', 'Grandfather'),
    ('uncle', 'Uncle'),
    ('aunt', 'Aunt'),
    ('sister', 'Sister'),
    ('brother', 'Brother'),
    ('guardian', 'Guardian'),
    (OTHER, 'Other'),
]

BUILT_DATES = (
    ('before_1980', 'Before 1980'),
    ('1980-1990', '1980-1990'),
    ('1991-2000', '1991-2000'),
    ('2001-2010', '2001-2010'),
    ('2011-2019', '2011-2019'),
    ('after_2019', 'After 2019'),
    ('i_dont_know', 'I don’t know'))

CAREGIVER_EDUCATION_LEVEL_CHOICES = (
    ('no_prim_male_caregiver', 'No primary male caregiver'),
    ('not_educated', 'Not educated'),
    ('primary', 'Primary'),
    ('secondary', 'Secondary'),
    ('tertiary', 'Tertiary')
)

HOUSE_YEAR_BUILT_CHOICES = (
    ('before_1980', 'Before 1980'),
    ('1980-1990', '1980-1990'),
    ("1991-2000", '1991-2000'),
    ("2001-2010", '2001-2010'),
    ("2011-2019", '2011-2019'),
    ("2019_above", '2019 and above'),
    (DONT_KNOW, 'I don’t know'),
)

BUSINESSES_RUN = (
    ('seamstress', 'Seamstress'),
    ('welding', 'Welding'),
    ('vehicle_repair', 'Vehicle repair'),
    ('furniture_construction', 'Furniture construction/repair'),
    ('selling', 'Selling'),
    ('painting', 'Painting'),
    (OTHER, 'Other'),
)
