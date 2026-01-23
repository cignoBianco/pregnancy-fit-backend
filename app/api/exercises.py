from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.database import get_session
from app.api.deps import get_current_user
from app.models.exercise import Exercise
from app.schemas.exercise import ExerciseCreate, ExerciseRead
from app.models.user import User

router = APIRouter(prefix="/exercises", tags=["exercises"])

@router.post("/", response_model=ExerciseCreate)
def create_exercise(
    data: ExerciseCreate,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),  # Todo: RBAC
):
    exercise = Exercise(**data.model_dump())
    session.add(exercise)
    session.commit()
    session.refresh(exercise)
    return exercise

@router.get("/", response_model=list[ExerciseRead])
def list_exercises(
    session: Session = Depends(get_session),
):
    return session.exec(
        select(Exercise).where(Exercise.is_active == True)
    ).all()

@router.get("/{exercise_id}", response_model=ExerciseRead)
def get_exercise(
    exercise_id: int,
    session: Session = Depends(get_session),
):
    exercise = session.get(Exercise, exercise_id)
    if not exercise:
        raise HTTPException(404, "Exercise not found")
    return exercise

@router.delete("/{exercise_id}")
def deactivate_exercise(
    exercise_id: int,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    exercise = session.get(Exercise, exercise_id)
    if not exercise:
        raise HTTPException(404, "Exercise not found")

    exercise.is_active = False
    session.add(exercise)
    session.commit()
    return {"status": "deactivated"}
