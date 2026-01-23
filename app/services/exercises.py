def filter_exercises(exercises, phase, equipment):
    return [
        e for e in exercises
        if e.allowed_phases.get(phase) in [True, "modified"]
        and set(e.equipment).intersection(equipment)
    ]