from fastapi import HTTPException
from pydantic import BaseModel, validator
from typing import List, Optional
from app.models.enums import EquipmentEnum, ContraindicationEnum, TrainingGoalEnum
from app.domain.pregnancy import PregnancyProgress
from datetime import date


class UserProfileBase(BaseModel):
    full_name: Optional[str]
    pregnancy_start_date: Optional[str]
    due_date: Optional[str]
    equipment: List[EquipmentEnum] = []
    contraindications: List[ContraindicationEnum] = []
    training_goals: List[TrainingGoalEnum] = []
    notes: Optional[str] = None

class UserProfileRead(UserProfileBase):
    id: int
    user_id: int
    current_phase: Optional[str]
    progress_weeks: Optional[int]

    class Config:
        from_attributes = True
        orm_mode = True

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


class UserProfileUpdate(BaseModel):
    full_name: Optional[str]
    pregnancy_start_date:Optional[date]
    due_date: Optional[date]
    equipment: Optional[List[str]]
    contraindications: Optional[List[str]]
    training_goals: Optional[List[TrainingGoalEnum]]
