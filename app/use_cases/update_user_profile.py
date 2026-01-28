from typing import Optional
from app.domain.pregnancy import PregnancyDates
from app.domain.repositories.profile_repository import ProfileRepository
from app.domain.profile import UserProfile


class UpdateUserProfile:
    def __init__(self, repo: ProfileRepository):
        self.repo = repo

    def execute(
        self,
        user_id: int,
        *,
        full_name: Optional[str] = None,
        pregnancy_start_date: Optional[str] = None,
        due_date: Optional[str] = None,
    ) -> UserProfile:

        profile = self.repo.get_by_user_id(user_id)

        if full_name is not None:
            profile.full_name = full_name

        if pregnancy_start_date is not None or due_date is not None:
            pregnancy = PregnancyDates.normalize(
                pregnancy_start_date=pregnancy_start_date or profile.pregnancy_start_date,
                due_date=due_date or profile.due_date,
            )
            profile.pregnancy_start_date = pregnancy.pregnancy_start_date
            profile.due_date = pregnancy.due_date

        self.repo.save(profile)
        return profile
