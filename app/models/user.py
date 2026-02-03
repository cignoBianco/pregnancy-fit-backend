from datetime import date
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Enum as SAEnum
from typing import Optional

from app.services.user_phase import calculate_phase
from app.models.enums import ExperienceLevel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str

    full_name: Optional[str] = None

    experience_level: Optional[ExperienceLevel] = Field(
        default=ExperienceLevel.beginner,
        sa_column=Column(
            SAEnum(
                ExperienceLevel,
                name="experiencelevel",
                create_type=False,  # ВАЖНО
            )
        )
    )

    is_active: bool = True
    role: str = Field(default="user")  # Todo: enum user | coach | admin

    profile: Optional["UserProfile"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"uselist": False}
    )
