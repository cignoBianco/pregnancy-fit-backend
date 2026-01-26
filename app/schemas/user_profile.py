from fastapi import HTTPException
from pydantic import BaseModel, validator
from typing import List, Optional
from app.models.enums import EquipmentEnum, ContraindicationEnum


class UserProfileBase(BaseModel):
    equipment: List[EquipmentEnum] = []
    contraindications: List[ContraindicationEnum] = []
    notes: Optional[str] = None

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
