from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import Optional

from app.core.database import get_session
from app.api.deps import get_current_user
from app.models.exercise import Exercise
from app.schemas.exercise import ExerciseCreate, ExerciseRead, ExerciseUpdate
from app.models.user import User
from app.models.enums import ExerciseCategory, PregnancyPhase, PhasePermission

router = APIRouter(prefix="/exercises", tags=["exercises"])

@router.post("/", response_model=ExerciseRead, status_code=201)
def create_exercise(
    data: ExerciseCreate,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),  # Todo: RBAC require coach/admin
):
    exercise = Exercise(**data.model_dump())
    session.add(exercise)
    session.commit()
    session.refresh(exercise)
    return exercise

@router.get("/", response_model=list[ExerciseRead])
def list_exercises(
    category: Optional[ExerciseCategory] = None,
    phase: Optional[PregnancyPhase] = None,
    equipment: Optional[str] = Query(None, description="#dumbbell"),
    session: Session = Depends(get_session),
):
    query = select(Exercise).where(Exercise.is_active == True)

    if category:
        query = query.where(Exercise.category == category)

    if equipment:
        query = query.where(
            Exercise.equipment.contains([equipment])
        )

    exercises = session.exec(query).all()

    if phase:
        exercises = [
            e for e in exercises
            if e.allowed_phases.get(phase) != "forbidden"
        ]

    return exercises

@router.get("/{exercise_id}", response_model=ExerciseRead)
def get_exercise(
    exercise_id: int,
    session: Session = Depends(get_session),
):
    exercise = session.get(Exercise, exercise_id)
    if not exercise:
        raise HTTPException(404, "Exercise not found")
    return exercise

@router.patch("/{exercise_id}", response_model=ExerciseRead)
def update_exercise(
    exercise_id: int,
    data: ExerciseUpdate,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    exercise = session.get(Exercise, exercise_id)
    if not exercise:
        raise HTTPException(404, "Exercise not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(exercise, field, value)

    session.add(exercise)
    session.commit()
    session.refresh(exercise)
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
