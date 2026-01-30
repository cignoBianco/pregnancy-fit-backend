from datetime import date
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB

from app.models.enums import EquipmentEnum, ContraindicationEnum, TrainingGoalEnum
from app.services.user_phase import calculate_phase



class UserProfile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(
        foreign_key="user.id",
        index=True,
        unique=True,
        nullable=False,
    )

    full_name: Optional[str] = None

    pregnancy_start_date: Optional[date] = None
    due_date: Optional[date] = None

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

    @property
    def current_phase(self) -> Optional[str]:
        if not self.pregnancy_start_date or not self.due_date:
            return None
        return calculate_phase(
            pregnancy_start_date=self.pregnancy_start_date,
            due_date=self.due_date,
        )
