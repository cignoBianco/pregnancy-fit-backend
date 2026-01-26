from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.core.database import get_session
from app.api.deps import get_current_user
from app.models.user import User
from app.models.user_profile import UserProfile
from app.schemas.user_profile import (
    UserProfileCreate,
    UserProfileRead,
    UserProfileUpdate,
)

router = APIRouter(prefix="/profile", tags=["profile"])

@router.get("/me", response_model=UserProfileRead)
def get_my_profile(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    profile = session.exec(
        select(UserProfile).where(UserProfile.user_id == user.id)
    ).first()

    if not profile:
        profile = UserProfile(user_id=user.id)
        session.add(profile)
        session.commit()
        session.refresh(profile)

    return profile


@router.put("/me", response_model=UserProfileRead)
def update_my_profile(
    data: UserProfileUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    profile = session.exec(
        select(UserProfile).where(UserProfile.user_id == user.id)
    ).first()

    if not profile:
        profile = UserProfile(user_id=user.id)

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(profile, key, value)

    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile
