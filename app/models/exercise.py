from sqlmodel import SQLModel, Field
from typing import List, Optional, Dict
from sqlalchemy import Column, JSON
from app.models.enums import ExerciseCategory

class Exercise(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field(index=True)
    category: ExerciseCategory
    is_active: bool = Field(default=True)

    primary_muscles: List[str] = Field(sa_column=Column(JSON))
    equipment: List[str] = Field(sa_column=Column(JSON))

    allowed_phases: Dict[str, str] = Field(
        sa_column=Column(JSON),
        description="phase -> allowed | modified | forbidden"
    )

    contraindications: List[str] = Field(sa_column=Column(JSON))
    base_rpe: int = Field(ge=1, le=10)
    base_sets: int
    base_reps: int

class PlannedWorkoutExercise(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    planned_workout_id: int = Field(foreign_key="plannedworkout.id")
    exercise_id: int = Field(foreign_key="exercise.id")
    sets: int
    reps: int
    rpe: int
