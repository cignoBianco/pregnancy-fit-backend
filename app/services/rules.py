from app.models.enums import PregnancyPhase

RULES = {
    PregnancyPhase.pregnancy_t1: {
        "strength_days": 2,
        "cardio_days": 2,
        "mobility_days": 1,
        "max_rpe": 7
    },
    PregnancyPhase.pregnancy_t2: {
        "strength_days": 2,
        "cardio_days": 2,
        "mobility_days": 1,
        "max_rpe": 6
    },
    PregnancyPhase.pregnancy_t3: {
        "strength_days": 1,
        "cardio_days": 3,
        "mobility_days": 2,
        "max_rpe": 6
    },
    PregnancyPhase.postpartum_0_6: {
        "strength_days": 0,
        "cardio_days": 2,
        "mobility_days": 3,
        "max_rpe": 4
    }
}