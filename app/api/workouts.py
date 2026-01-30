from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from datetime import date, timedelta
from typing import Optional

from app.core.database import get_session
from app.api.deps import get_current_user
from app.infrastructure.repositories.plan_repository_sql import SQLPlanRepository
from app.models.user import User
from app.models.workout import CompletedWorkout, PlannedWorkoutRead

router = APIRouter(prefix="/workouts", tags=["workouts"])

@router.post("/{planned_id}/complete")
def complete_workout(planned_id: int, rpe_actual: int = 7, mood: str = "good", user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    planned = session.get(PlannedWorkoutRead, planned_id)
    if not planned or planned.plan.user_id != user.id:
        raise HTTPException(404, "Planned workout not found")

    workout = CompletedWorkout(
        planned_workout_id=planned_id,
        user_id=user.id,
        date=date.today(),
        rpe_actual=rpe_actual,
        mood=mood
    )
    session.add(workout)
    session.commit()
    return {"status": "completed", "completed_id": completed.id}


@router.get("/completed")
def list_completed_workouts(
    start: Optional[date] = None,
    end: Optional[date] = None,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user)
):
    repo = SQLPlanRepository(session)
    completed = repo.get_completed(user.id)
    if start:
        completed = [c for c in completed if c.date >= start]
    if end:
        completed = [c for c in completed if c.date <= end]
    return completed

@router.get("/planned")
def list_planned_workouts(
    start: Optional[date] = None,
    end: Optional[date] = None,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user)
):
    repo = SQLPlanRepository(session)
    plans = repo.get_user_plans(user.id)
    workouts = []
    for plan in plans:
        for w in plan.workouts:
            if start and w.date < start:
                continue
            if end and w.date > end:
                continue
            workouts.append(w)
    return workouts
