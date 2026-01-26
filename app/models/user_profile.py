from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB

from app.models.enums import EquipmentEnum, ContraindicationEnum, TrainingGoalEnum


class UserProfile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(
        foreign_key="user.id",
        index=True,
        unique=True,
        nullable=False,
    )

    equipment: List[str] = Field(
        sa_column=Column(JSONB),
        default_factory=list,
        description="Available equipment for workouts"
    )

    contraindications: List[str] = Field(
        sa_column=Column(JSONB),
        default_factory=list,
        description="Medical or physical contraindications"
    )

    training_goals: List[TrainingGoalEnum] = Field(
        sa_column=Column(JSONB),
        default_factory=list,
    )

    notes: Optional[str] = None

    user: "User" = Relationship(back_populates="profile")
