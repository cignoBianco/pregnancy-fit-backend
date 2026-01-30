from sqlmodel import Session, select
from app.models.plan import TrainingPlan, PlannedWorkout
from app.models.exercise import PlannedWorkoutExercise
from app.models.workout import CompletedWorkout
from typing import Optional
from datetime import date, timedelta


class SQLPlanRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_user_plans(self, user_id: int) -> list[TrainingPlan]:
        return self.session.exec(
            select(TrainingPlan).where(TrainingPlan.user_id == user_id)
        ).all()

    def get_plan(self, plan_id: int) -> Optional[TrainingPlan]:
        return self.session.get(TrainingPlan, plan_id)

    def save_plan(self, plan: TrainingPlan) -> TrainingPlan:
        self.session.add(plan)
        self.session.commit()
        self.session.refresh(plan)
        return plan

    def delete_plan(self, plan: TrainingPlan):
        self.session.delete(plan)
        self.session.commit()

    def get_workouts(self, plan_id: int) -> list[PlannedWorkout]:
        return self.session.exec(
            select(PlannedWorkout).where(PlannedWorkout.plan_id == plan_id)
        ).all()

    def save_workout(self, workout: PlannedWorkout) -> PlannedWorkout:
        self.session.add(workout)
        self.session.commit()
        self.session.refresh(workout)
        return workout

    def save_workout_exercises(self, exercises: list[PlannedWorkoutExercise]):
        for ex in exercises:
            self.session.add(ex)
        self.session.commit()

    def mark_completed(self, completed: CompletedWorkout) -> CompletedWorkout:
        self.session.add(completed)
        self.session.commit()
        self.session.refresh(completed)
        return completed

    def get_completed(self, user_id: int) -> list[CompletedWorkout]:
        return self.session.exec(
            select(CompletedWorkout).where(CompletedWorkout.user_id == user_id)
        ).all()

    def add_or_commit_plan(self, user_id: int, start_date: date, weeks: int, phase: str) -> TrainingPlan:
        end_date = start_date + timedelta(weeks=weeks)

        plan = TrainingPlan(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            phase=phase,
        )
        self.session.add(plan)
        self.session.commit()
        self.session.refresh(plan)
        return plan