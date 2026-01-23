from enum import Enum

class ExerciseCategory(str, Enum):
    strength = "strength"
    cardio = "cardio"
    mobility = "mobility"
    breathing = "breathing"

PREGNANCY_T1 = "pregnancy_t1"
PREGNANCY_T2 = "pregnancy_t2"
PREGNANCY_T3 = "pregnancy_t3"
POSTPARTUM_0_6 = "postpartum_0_6"
POSTPARTUM_6_12 = "postpartum_6_12"