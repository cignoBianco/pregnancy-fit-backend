from typing import List, Dict
from pydantic import BaseModel
from app.models.enums import ExerciseCategory

class ExerciseBase(BaseModel):
    name: str
    category: ExerciseCategory
    primary_muscles: List[str]
    equipment: List[str]
    allowed_phases: Dict[str, str]
    contraindications: List[str]
    base_rpe: int
    base_sets: int
    base_reps: int


class ExerciseCreate(ExerciseBase):
    pass


class ExerciseRead(ExerciseBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
