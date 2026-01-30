from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.api.deps import get_current_user
from app.core.database import get_session
from app.schemas.user import UserUpdate, UserRead
from app.models.user import User
from app.use_cases.update_user_profile import UpdateUserProfile
from app.infrastructure.repositories.profile_repository_sql import SQLProfileRepository

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
def get_me(user: User = Depends(get_current_user)):
    return UserRead.from_orm(user)


@router.put("/me", response_model=UserRead)
def update_me(
    data: UserUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(user, field, value)
    session.add(user)
    session.commit()
    session.refresh(user)
    return UserRead.from_orm(user)
