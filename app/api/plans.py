from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.domain.profile import UserProfile as DomainUserProfile

from datetime import date, timedelta
from typing import List

from app.models.exercise import PlannedWorkoutExercise, Exercise

from app.api.deps import get_current_user
from app.core.database import get_session
from app.models.plan import TrainingPlan, PlannedWorkout
from app.models.user import User
from app.models.user_profile import UserProfile
from app.models.workout import PlannedWorkoutRead
from app.services.plan_generator import generate_training_plan, phase_config, build_workout_exercises
from app.infrastructure.repositories.plan_repository_sql import SQLPlanRepository
from app.use_cases.generate_training_plan import GenerateTrainingPlanUseCase
from app.domain.pregnancy import PregnancyProgress


router = APIRouter(prefix="/plans", tags=["plans"])

@router.get("/me")
def get_my_plans(session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    repo = SQLPlanRepository(session)
    return repo.get_user_plans(user.id)

@router.post("/plans/generate", response_model=List[PlannedWorkoutRead])
def generate_plan(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    db_profile = session.exec(
        select(UserProfile).where(UserProfile.user_id == user.id)
    ).first()

    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    domain_profile = DomainUserProfile(
        user_id=db_profile.user_id,
        full_name=db_profile.full_name,
        pregnancy_start_date=db_profile.pregnancy_start_date,
        due_date=db_profile.due_date,
        equipment=db_profile.equipment,
        contraindications=db_profile.contraindications,
        training_goals=db_profile.training_goals,
        notes=db_profile.notes,
    )

    exercises = session.exec(select(Exercise)).all()

    plan_repo = SQLPlanRepository(session)
    use_case = GenerateTrainingPlanUseCase(
        plan_repo=plan_repo,
        exercises=exercises,
    )

    workouts = use_case.execute(domain_profile)

    return [PlannedWorkoutRead.from_orm(w) for w in workouts]


@router.delete("/{plan_id}")
def delete_plan(plan_id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    repo = SQLPlanRepository(session)
    plan = repo.get_plan(plan_id, user.id)
    if not plan:
        raise HTTPException(404, "Plan not found")
    repo.delete_plan(plan)
    return {"status": "deleted"}
