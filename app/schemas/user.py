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


class UserRead(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    experience_level: Optional[ExperienceLevel]

    class Config:
        from_attributes = True
