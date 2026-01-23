from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import date

class TrainingPlan(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    start_date: date
    end_date: date
    phase: str

class PlannedWorkout(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    plan_id: int = Field(foreign_key="trainingplan.id", index=True)
    date: date
    workout_type: str
    duration: int

    exercises: List["PlannedWorkoutExercise"] = Relationship(
        back_populates="planned_workout"
    )
