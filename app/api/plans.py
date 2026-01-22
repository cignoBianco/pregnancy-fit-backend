from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from datetime import date, timedelta

from app.api.deps import get_current_user
from app.core.database import get_session
from app.models.plan import TrainingPlan, PlannedWorkout
from app.models.user import User
from app.services.plan_generator import generate_plan, phase_config

router = APIRouter(prefix="/plans", tags=["plans"])

@router.post("/generate")
def generate(
    start_date: date,
    weeks: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Проверка на допустимые недели
    if weeks < 1 or weeks > 40:
        raise HTTPException(status_code=400, detail="Weeks must be between 1 and 40")

    end_date = start_date + timedelta(weeks=weeks)

    # if weeks <= 12:
    #     phase = "first_trimester"
    # elif weeks <= 28:
    #     phase = "second_trimester"
    # else:
    #     phase = "third_trimester"

    plan = TrainingPlan(
        user_id=user.id,
        start_date=start_date,
        end_date=start_date,
        phase=user.current_phase
    )
    session.add(plan)
    session.commit()
    session.refresh(plan)

    workouts = generate_plan(None, start_date, weeks)
    for w in workouts:
        session.add(PlannedWorkout(plan_id=plan.id, **w))

    session.commit()
    return { "plan_id": plan.id }
