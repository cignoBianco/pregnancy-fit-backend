from datetime import date
from sqlmodel import SQLModel, Field
from typing import Optional

from app.services.user_phase import calculate_phase


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str

    full_name: Optional[str] = None

    experience_level: str
    pregnancy_start_date: Optional[date] = None
    due_date: Optional[date] = None

    is_active: bool = True
    role: str = Field(default="user")  # Todo: enum user | coach | admin

    @property
    def current_phase(self) -> Optional[str]:
        return calculate_phase(
            pregnancy_start_date=self.pregnancy_start_date,
            due_date=self.due_date,
        )