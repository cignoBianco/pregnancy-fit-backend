from enum import Enum

class ExerciseCategory(str, Enum):
    strength = "strength"
    cardio = "cardio"
    mobility = "mobility"
    breathing = "breathing"

    @property
    def label(self):
        return {
            "strength": "Strength",
            "cardio": "Cardio",
            "mobility": "Mobility",
            "breathing": "Breathing",
        }[self.value]


class PregnancyPhase(str, Enum):
    pregnancy_t1 = "pregnancy_t1"
    pregnancy_t2 = "pregnancy_t2"
    pregnancy_t3 = "pregnancy_t3"
    postpartum_0_6 = "postpartum_0_6"
    postpartum_6_12 = "postpartum_6_12"

    @property
    def label(self):
        return {
            "pregnancy_t1": "1st Trimester",
            "pregnancy_t2": "2nd Trimester",
            "pregnancy_t3": "3rd Trimester",
            "postpartum_0_6": "Postpartum from 0 to 6 months",
            "postpartum_6_12": "Postpartum from 6 to 12 months",
        }[self.value]


class PhasePermission(str, Enum):
    allowed = "allowed"
    modified = "modified"
    forbidden = "forbidden"

    @property
    def label(self):
        return {
            "allowed": "Allowed",
            "modified": "Modified",
            "forbidden": "Forbidden",
        }[self.value]


class EquipmentEnum(str, Enum):
    dumbbells = "dumbbells"
    resistance_band = "resistance_band"
    pool = "pool"
    mat = "mat"

    @property
    def label(self):
        return {
            "dumbbells": "Dumbbells",
            "resistance_band": "Resistance band",
            "pool": "Pool",
            "mat": "Mat",
        }[self.value]


class ContraindicationEnum(str, Enum):
    pelvic_pain = "pelvic_pain"
    diastasis = "diastasis"
    high_bp = "high_bp"
    placenta_previa = "placenta_previa"

    @property
    def label(self):
        return {
            "pelvic_pain": "Pelvic pain",
            "diastasis": "Diastasis",
            "high_bp": "High BP",
            "placenta_previa": "Placenta previa",
        }[self.value]


class ExperienceLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"

    @property
    def label(self):
        return {
            "beginner": "Beginner",
            "intermediate": "Intermediate",
            "advanced": "Advanced",
        }[self.value]


class TrainingGoalEnum(str, Enum):
    maintain_fitness = "Maintain fitness"
    reduce_pain = "Reduce pain"
    prepare_for_birth = "Prepare for birth"
    postpartum_recovery = "Postpartum recovery"
