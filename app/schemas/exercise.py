from typing import List, Dict, Optional
from pydantic import BaseModel
from sqlmodel import Field
from app.models.enums import ExerciseCategory, PregnancyPhase, PhasePermission

class ExerciseBase(BaseModel):
    name: str
    category: ExerciseCategory
    primary_muscles: List[str]
    equipment: List[str]
    allowed_phases: Dict[PregnancyPhase, PhasePermission]
    contraindications: List[str]
    base_rpe: int = Field(ge=1, le=10)
    base_sets: int = Field(ge=1)
    base_reps: int = Field(ge=1)

class ExerciseUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[ExerciseCategory] = None
    primary_muscles: Optional[List[str]] = None
    equipment: Optional[List[str]] = None
    allowed_phases: Optional[Dict[PregnancyPhase, PhasePermission]] = None
    contraindications: Optional[List[str]] = None
    base_rpe: Optional[int] = None
    base_sets: Optional[int] = None
    base_reps: Optional[int] = None
    is_active: Optional[bool] = None

class ExerciseCreate(ExerciseBase):
    pass


class ExerciseRead(ExerciseBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
