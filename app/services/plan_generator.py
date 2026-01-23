from datetime import  datetime, date, timedelta
from app.models.user import User
from app.models.exercise import Exercise, PlannedWorkoutExercise
from app.services.exercises import filter_exercises
from app.services.rules import RULES
import random

phase_config = {
    "first_trimester": {
        "workout_types": ["strength", "cardio", "yoga"],
        "duration_range": (40, 50),
        "notes": "Можно поддерживать привычный уровень активности. Избегать риска падений."
    },
    "second_trimester": {
        "workout_types": ["strength", "prenatal_yoga", "walking", "pelvic_floor"],
        "duration_range": (30, 45),
        "notes": "Избегать упражнений на спине. Акцент на тазовое дно и стабильность."
    },
    "third_trimester": {
        "workout_types": ["prenatal_yoga", "walking", "breathing", "swimming"],
        "duration_range": (20, 35),
        "notes": "Снижаем интенсивность. Фокус на расслабление, дыхание и комфорт."
    }
}

def build_workout_exercises(
    *,
    exercises: list[Exercise],
    phase: str,
    equipment: list[str],
) -> list[dict]:
    filtered = filter_exercises(exercises, phase, equipment)

    selected = random.sample(filtered, k=min(4, len(filtered)))

    rules = RULES.get(phase, {})
    max_rpe = rules.get("max_rpe", 7)

    result = []

    for ex in selected:
        rpe = min(ex.base_rpe, max_rpe)

        result.append({
            "exercise_id": ex.id,
            "sets": ex.base_sets,
            "reps": ex.base_reps,
            "rpe": rpe,
            "is_modified": ex.allowed_phases.get(phase) == "modified"
        })

    return result

def generate_training_plan(
    *,
    phase: str,
    start_date: date,
    weeks: int,
) -> list[dict]:
    print('111', phase)
    config = phase_config[phase]
    types = config["workout_types"]
    min_dur, max_dur = config["duration_range"]

    plan = []

    for w in range(weeks):
        duration = min(max_dur, min_dur + w % 3 * 5)

        plan.append({
            "date": start_date + timedelta(weeks=w),
            "workout_type": types[w % len(types)],
            "duration": duration,
        })

    return plan
