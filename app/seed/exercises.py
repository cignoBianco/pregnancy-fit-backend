EXERCISES = [
    {
        "name": "Goblet Squat",
        "category": "strength",
        "primary_muscles": ["quads", "glutes"],
        "equipment": ["dumbbell"],
        "base_sets": 3,
        "base_reps": 10,
        "base_rpe": 6,
        "allowed_phases": {
            # allowed | modified | forbidden
            "pregnancy_t1": "allowed",
            "pregnancy_t2": "modified",
            "pregnancy_t3": "forbidden",
            "postpartum_0_6": "modified",
            "postpartum_6_12": "allowed"
        },
        "contraindications": ["severe_diastasis"]
    },
    {
        "name": "Swimming",
        "category": "cardio",
        "primary_muscles": ["full_body"],
        "equipment": ["pool"],
        "base_sets": 1,
        "base_reps": 30,
        "base_rpe": 5,
        "allowed_phases": {
            "pregnancy_t1": "allowed",
            "pregnancy_t2": "modified",
            "pregnancy_t3": "forbidden",
            "postpartum_0_6": "modified",
            "postpartum_6_12": "allowed"
        },
        "contraindications": []
    }
]