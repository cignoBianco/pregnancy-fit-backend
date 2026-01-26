from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.api.deps import get_current_user
from app.core.database import get_session
from app.schemas.user import UserUpdate, UserRead
from app.models.user import User
from app.use_cases.update_user_profile import UpdateUserProfile

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
def get_me(user: User = Depends(get_current_user)):
    return user


@router.put("/me", response_model=UserRead)
def update_me(
    data: UserUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    updates = data.model_dump(exclude_unset=True)

    if not updates:
        raise HTTPException(
            status_code=400,
            detail="At least one field must be provided"
        )

    try:
        return UpdateUserProfile(session).execute(
            user=user,
            **data.model_dump(exclude_unset=True)
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
