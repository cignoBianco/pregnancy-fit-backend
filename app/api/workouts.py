from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from sqlmodel import Session
from app.models.workout import CompletedWorkout
from app.models.user import User
from app.core.database import get_session
from datetime import date

router = APIRouter(prefix="/workouts", tags=["workouts"])

@router.post("/{planned_id}/complete")
def complete(planned_id: int, session: Session = Depends(get_session),
    user: User = Depends(get_current_user),  # Todo: RBAC require coach/admin
):
    workout = CompletedWorkout(
        planned_workout_id=planned_id,
        user_id=user.id,
        date=date.today(),
        rpe_actual=7,
        mood="good"
    )
    session.add(workout)
    session.commit()
    return {"status": "completed"}
