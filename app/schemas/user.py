from pydantic import BaseModel, EmailStr, Field, validator
from datetime import date
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)
    experience_level: str
    pregnancy_start_date: Optional[date] = None
    due_date: Optional[date] = None

    @validator("password")
    def password_must_be_valid(cls, v):
        if len(v.encode('utf-8')) > 72:
            raise ValueError("Password exceeds 72 bytes after UTF-8 encoding")
        return v

class Token(BaseModel):
    access_token: str
    token_type: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    pregnancy_start_date: Optional[date] = None
    due_date: Optional[date] = None
    equipment: Optional[List[str]] = None
    contraindications: Optional[List[str]] = None


class UserRead(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    pregnancy_start_date: Optional[date]
    due_date: Optional[date]
    equipment: List[str]
    contraindications: List[str]
    current_phase: Optional[str]

    class Config:
        from_attributes = True
