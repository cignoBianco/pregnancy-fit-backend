from app.models.exercise import Exercise
from app.models.enums import PregnancyPhase, PhasePermission

def filter_exercises(
    exercises: list[Exercise],
    phase: PregnancyPhase,
    equipment: list[str],
):
    result = []

    for e in exercises:
        permission = e.allowed_phases.get(phase)

        if permission == PhasePermission.forbidden:
            continue

        if not set(e.equipment).intersection(equipment):
            continue

        result.append(e)

    return result
