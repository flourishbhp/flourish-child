from django.utils.translation import ugettext_lazy as _
from edc_constants.constants import ALIVE, DEAD, UNKNOWN, PARTICIPANT, \
    NOT_APPLICABLE
from edc_constants.constants import FAILED_ELIGIBILITY, YES, NO, OTHER, \
    ON_STUDY, OFF_STUDY, DONT_KNOW, MALE, FEMALE
from edc_constants.constants import NEG, POS, IND
from edc_visit_tracking.constants import MISSED_VISIT, COMPLETED_PROTOCOL_VISIT
from edc_visit_tracking.constants import SCHEDULED, UNSCHEDULED, LOST_VISIT

from .constants import BREASTFEED_ONLY

ALIVE_DEAD_UNKNOWN = (
    (ALIVE, 'Alive'),
    (DEAD, 'Dead'),
    (UNKNOWN, 'Unknown'),
)

ANSWERER = (
    ('caregiver', 'Caregiver'),
    ('child_adolescent', 'Child/Adolescent'),
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
     'Pentavalent Vaccine (Contains DPT, Hepatitis B and Haemophilus Influenza B Vaccine)'),
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
     'Pentavalent Vaccine (Contains DPT, Hepatitis B and Haemophilus Influenza B Vaccine)'),
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

PHYS_ACTIVITY_TIME = (
    ('specify_hrs_mins', 'Hours and minutes per day (specify)'),
    (DONT_KNOW, 'Don\'t know/Not sure')
)

POS_NEG_IND = (
    (POS, 'Positive'),
    (NEG, 'Negative'),
    (IND, 'Indeterminate')
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
    ('public', 'Public'),
    ('private', 'Private'),
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
    ('pre-traveling_screening ', 'Pre-Traveling screening '),
    ('routine_testing ', 'Routine testing '),
    ('contact_tracing', 'Contact tracing'),
    (OTHER, 'Other')
)

POS_NEG_PENDING_UNKNOWN = (
    (POS, 'Positive'),
    (NEG, 'Negative'),
    ('PENDING', 'Pending'),
    (UNKNOWN, 'Unknown'),
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

