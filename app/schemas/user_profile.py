from fastapi import HTTPException
from pydantic import BaseModel, validator
from typing import List, Optional
from app.models.enums import EquipmentEnum, ContraindicationEnum, TrainingGoalEnum
from app.domain.pregnancy import PregnancyProgress


class UserProfileBase(BaseModel):
    id: int
    user_id: int

    full_name: Optional[str]
    pregnancy_start_date: Optional[str]
    due_date: Optional[str]

    equipment: List[EquipmentEnum] = []
    contraindications: List[ContraindicationEnum] = []
    training_goals: List[TrainingGoalEnum] = []
    notes: Optional[str] = None

    current_phase: Optional[str]
    progress_weeks: Optional[int]

    @validator("equipment")
    def no_duplicates(cls, v):
        if len(v) != len(set(v)):
            raise HTTPException(
                status_code=422,
                detail="Duplicate equipment values are not allowed",
            )
        return v


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileUpdate(UserProfileBase):
    pass


class UserProfileRead(UserProfileBase):
    id: int

    class Config:
        from_attributes = True
