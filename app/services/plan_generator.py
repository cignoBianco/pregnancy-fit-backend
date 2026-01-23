from datetime import  datetime, date, timedelta
from app.models.user import User

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

def generate_plan(user: User, start_date: date, weeks):
    plan = []

    # Установим дефолт, если phase не передан (на всякий случай)
    # if not phase or phase not in phase_config:
    #     phase = "first_trimester"

    phase = user.current_phase

    config = phase_config[phase]
    workout_types = config["workout_types"]
    min_duration, max_duration = config["duration_range"]

    for w in range(weeks):
        week_start = start_date + timedelta(weeks=w)

        strength = exercises[:4]
        cardio = exercises[4:6]

        # Случайный выбор типа тренировки из доступных
        workout_type = workout_types[w % len(workout_types)]

        # Случайная длительность в диапазоне (можно сделать фиксированной, если нужно)
        duration = min_duration + (w % 3) * 5  # плавное снижение в 3-м триместре
        if duration > max_duration:
            duration = max_duration

        plan.append({
            "date": week_start,
            "workout_type": workout_type,
            "duration": duration,
            "workouts": [
                {"type": "strength", "exercises": strength},
                {"type": "cardio", "exercises": cardio}
            ]
        })

    return plan
