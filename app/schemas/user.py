from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, Field, validator, model_validator
from datetime import date
from typing import Optional, List

from app.models.enums import ExperienceLevel


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)
    experience_level: Optional[ExperienceLevel] = ExperienceLevel.beginner
    pregnancy_start_date: Optional[date] = None
    due_date: Optional[date] = None

    @validator("password")
    def password_must_be_valid(cls, v):
        if len(v.encode('utf-8')) > 72:
            raise HTTPException(
                status_code=422,
                detail="Password exceeds 72 bytes after UTF-8 encoding",
            )
        return v

class Token(BaseModel):
    access_token: str
    token_type: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    pregnancy_start_date: Optional[date] = None
    due_date: Optional[date] = None

    # @model_validator(mode="after")
    # def validate_dates(self):
    #     psd = self.pregnancy_start_date
    #     dd = self.due_date

    #     if psd and dd:
    #         expected_dd = psd + timedelta(weeks=40)
    #         if abs((expected_dd - dd).days) > 7:
    #             raise ValueError(
    #                 "pregnancy_start_date and due_date contradict each other"
    #             )

    #     return self


class UserRead(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    pregnancy_start_date: Optional[date]
    due_date: Optional[date]
    current_phase: Optional[str]

    class Config:
        from_attributes = True
