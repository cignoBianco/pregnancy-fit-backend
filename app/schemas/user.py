from pydantic import BaseModel, EmailStr, Field, validator

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)
    experience_level: str
    current_phase: str

    @validator("password")
    def password_must_be_valid(cls, v):
        if len(v.encode('utf-8')) > 72:
            raise ValueError("Password exceeds 72 bytes after UTF-8 encoding")
        return v

class Token(BaseModel):
    access_token: str
    token_type: str