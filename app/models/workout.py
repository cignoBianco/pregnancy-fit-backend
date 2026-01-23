from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import date

class CompletedWorkout(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    planned_workout_id: Optional[int] = Field(foreign_key="plannedworkout.id")
    user_id: int = Field(foreign_key="user.id")
    date: date
    rpe_actual: int
    mood: str

class PlannedWorkoutExerciseRead(SQLModel):
    exercise_id: int
    name: str
    sets: int
    reps: int
    rpe: int

class PlannedWorkoutRead(SQLModel):
    id: int
    date: str
    workout_type: str
    duration: int
    exercises: List[PlannedWorkoutExerciseRead]