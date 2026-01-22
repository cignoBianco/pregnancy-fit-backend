from sqlmodel import SQLModel, Field
from typing import List, Optional
from sqlalchemy import Column, JSON

class Exercise(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    category: str  # strength, cardio, mobility
    primary_muscles: List[str] = Field(sa_column=Column(JSON))
    equipment: List[str] = Field(sa_column=Column(JSON))
    allowed_phases: dict = Field(sa_column=Column(JSON))
    contraindications: List[str] = Field(sa_column=Column(JSON))
    base_rpe: int
    base_sets: int
    base_reps: int

class PlannedWorkoutExercise(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    planned_workout_id: int = Field(foreign_key="plannedworkout.id")
    exercise_id: int = Field(foreign_key="exercise.id")
    sets: int
    reps: int
    rpe: int
