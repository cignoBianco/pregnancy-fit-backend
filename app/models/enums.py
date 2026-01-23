from enum import Enum

class ExerciseCategory(str, Enum):
    strength = "strength"
    cardio = "cardio"
    mobility = "mobility"
    breathing = "breathing"

class PregnancyPhase(str, Enum):
    pregnancy_t1 = "pregnancy_t1"
    pregnancy_t2 = "pregnancy_t2"
    pregnancy_t3 = "pregnancy_t3"
    postpartum_0_6 = "postpartum_0_6"
    postpartum_6_12 = "postpartum_6_12"

class PhasePermission(str, Enum):
    allowed = "allowed"
    modified = "modified"
    forbidden = "forbidden"
