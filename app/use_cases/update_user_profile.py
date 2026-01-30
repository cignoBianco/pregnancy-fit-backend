from typing import Optional
from app.domain.pregnancy import PregnancyDates
from app.domain.repositories.profile_repository import ProfileRepository
from app.domain.profile import UserProfile


class UpdateUserProfile:
    def __init__(self, repo: ProfileRepository):
        self.repo = repo

    def execute(self, user_id: int, **kwargs) -> UserProfile:
        profile = self.repo.get_by_user_id(user_id)

        if kwargs.get("full_name") is not None:
            profile.full_name = kwargs["full_name"]

        if kwargs.get("pregnancy_start_date") is not None or kwargs.get("due_date") is not None:
            profile.update_pregnancy_dates(
                kwargs.get("pregnancy_start_date"),
                kwargs.get("due_date"),
            )

        self.repo.save(profile)
        return profile
