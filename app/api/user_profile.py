from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.core.database import get_session
from app.api.deps import get_current_user
from app.models.user import User
from app.models.user_profile import UserProfile
from app.schemas.user_profile import (
    UserProfileCreate,
    UserProfileRead,
    UserProfileUpdate
)
from app.infrastructure.repositories.profile_repository_sql import (
    SQLProfileRepository,
)
from app.domain.pregnancy import PregnancyProgress
from app.use_cases.update_user_profile import UpdateUserProfile


router = APIRouter(prefix="/profile", tags=["profile"])

@router.get("/me", response_model=UserProfileRead)
def get_my_profile(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    repo = SQLProfileRepository(session)
    profile = repo.get_by_user_id(user.id)

    progress = PregnancyProgress.from_dates(
        profile.pregnancy_start_date,
        profile.due_date
    )

    return UserProfileRead(
        **profile.model_dump(),
        current_phase=progress.current_phase,
        progress_weeks=progress.weeks_progress,
    )


@router.put("/me", response_model=UserProfileRead)
def update_my_profile(
    data: UserProfileUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    repo = SQLProfileRepository(session)
    use_case = UpdateUserProfile(repo)

    profile = use_case.execute(
        user_id=user.id,
        **data.model_dump(exclude_unset=True)
    )
    return profile

