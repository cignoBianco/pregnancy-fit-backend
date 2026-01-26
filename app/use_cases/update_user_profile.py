from dataclasses import dataclass
from typing import Optional
from sqlmodel import Session

from app.models.user import User
from app.domain.pregnancy import PregnancyDates


@dataclass
class UpdateUserProfile:
    session: Session

    def __init__(self, repo: ProfileRepository):
        self.repo = repo

    def execute(
        self,
        user: User,
        *,
        full_name: Optional[str] = None,
        pregnancy_start_date: Optional[str] = None,
        due_date: Optional[str] = None,
    ) -> User:

        updates = {
            "full_name": full_name,
            "pregnancy_start_date": pregnancy_start_date,
            "due_date": due_date,
        }

        updates = {k: v for k, v in updates.items() if v is not None}

        has_psd = "pregnancy_start_date" in updates
        has_dd = "due_date" in updates

        if has_psd or has_dd:
            if has_psd and has_dd:
                pregnancy = PregnancyDates.normalize(
                    updates["pregnancy_start_date"],
                    updates["due_date"],
                )
            elif has_psd:
                pregnancy = PregnancyDates.normalize(
                    updates["pregnancy_start_date"],
                    None,
                )
            else:
                pregnancy = PregnancyDates.normalize(
                    None,
                    updates["due_date"],
                )

            user.pregnancy_start_date = pregnancy.pregnancy_start_date
            user.due_date = pregnancy.due_date

        if "full_name" in updates:
            user.full_name = updates["full_name"]

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user
