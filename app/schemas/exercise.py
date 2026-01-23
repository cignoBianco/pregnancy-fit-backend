from typing import List, Dict
from pydantic import BaseModel
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
    name: str | None = None
    category: ExerciseCategory | None = None
    primary_muscles: List[str] | None = None
    equipment: List[str] | None = None
    allowed_phases: Dict[PregnancyPhase, PhasePermission] | None = None
    contraindications: List[str] | None = None
    base_rpe: int | None = None
    base_sets: int | None = None
    base_reps: int | None = None
    is_active: bool | None = None

class ExerciseCreate(ExerciseBase):
    pass


class ExerciseRead(ExerciseBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
