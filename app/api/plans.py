from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from datetime import date, timedelta

from app.models.exercise import PlannedWorkoutExercise, Exercise

from app.api.deps import get_current_user
from app.core.database import get_session
from app.models.plan import TrainingPlan, PlannedWorkout
from app.models.user import User
from app.services.plan_generator import generate_training_plan, phase_config, build_workout_exercises

router = APIRouter(prefix="/plans", tags=["plans"])

@router.post("/generate")
def generate(
    start_date: date,
    weeks: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    plan = TrainingPlan(
        user_id=user.id,
        start_date=start_date,
        end_date=start_date + timedelta(weeks=weeks),
        phase=user.current_phase
    )
    session.add(plan)
    session.commit()
    session.refresh(plan)

    all_exercises = session.exec(
        select(Exercise).where(Exercise.is_active == True)
    ).all()

    current_phase = user.current_phase
    if current_phase not in ["first_trimester", "second_trimester", "third_trimester"]:
        if weeks <= 12:
            current_phase = "first_trimester"
        elif weeks <= 28:
            current_phase = "second_trimester"
        else:
            current_phase = "third_trimester"

    workouts = generate_training_plan(phase=current_phase, start_date=start_date, weeks=weeks)

    for w in workouts:
        pw = PlannedWorkout(
            plan_id=plan.id,
            date=w["date"],
            workout_type=w["workout_type"],
            duration=w["duration"],
        )
        session.add(pw)
        session.commit()
        session.refresh(pw)

        pw_exercises = build_workout_exercises(
            exercises=all_exercises,
            phase=current_phase,
            equipment=["dumbbell", "pool"],  # Todo: from profile
        )

        for ex in pw_exercises:
            session.add(
                PlannedWorkoutExercise(
                    planned_workout_id=pw.id,
                    **ex
                )
            )

    session.commit()
    return {"plan_id": plan.id}
