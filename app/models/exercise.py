from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional, Dict
from sqlalchemy import Column, JSON
from app.models.enums import ExerciseCategory, PregnancyPhase, PhasePermission
from sqlalchemy.dialects.postgresql import JSONB

class Exercise(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field(index=True, min_length=2)
    category: ExerciseCategory
    is_active: bool = Field(default=True)

    primary_muscles: List[str] = Field(sa_column=Column(JSONB))
    equipment: list[str] = Field(
        sa_column=Column(JSONB),
        description="List of required equipment"
    )

    allowed_phases: Dict[PregnancyPhase, PhasePermission] = Field(
        sa_column=Column(JSONB),
        description="phase -> allowed | modified | forbidden"
    )

    contraindications: List[str] = Field(sa_column=Column(JSONB))
    base_rpe: int = Field(ge=1, le=10)
    base_sets: int = Field(ge=1)
    base_reps: int = Field(ge=1)

class PlannedWorkoutExercise(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    planned_workout_id: int = Field(foreign_key="plannedworkout.id", index=True)
    exercise_id: int = Field(foreign_key="exercise.id", index=True)
    sets: int = Field(ge=1)
    reps: int = Field(ge=1)
    rpe: int = Field(ge=1, le=10)

    is_modified: bool = Field(default=False)

    planned_workout: Optional["PlannedWorkout"] = Relationship(
        back_populates="exercises"
    )