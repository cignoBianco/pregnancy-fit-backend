from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.api.deps import get_current_user
from app.core.database import get_session
from app.schemas.user import UserUpdate, UserRead
from app.models.user import User
from app.domain.pregnancy import PregnancyDates

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

    has_psd = "pregnancy_start_date" in updates
    has_dd = "due_date" in updates
    try:
        if has_psd and has_dd:
            pregnancy = PregnancyDates.normalize(
                pregnancy_start_date=updates["pregnancy_start_date"],
                due_date=updates["due_date"],
            )

        elif has_psd:
            pregnancy = PregnancyDates.normalize(
                pregnancy_start_date=updates["pregnancy_start_date"],
                due_date=None,
            )

        elif has_dd:
            pregnancy = PregnancyDates.normalize(
                pregnancy_start_date=None,
                due_date=updates["due_date"],
            )

        else:
            pregnancy = PregnancyDates(
                user.pregnancy_start_date,
                user.due_date,
            )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    user.pregnancy_start_date = pregnancy.pregnancy_start_date
    user.due_date = pregnancy.due_date

    for field, value in updates.items():
        if field not in {"pregnancy_start_date", "due_date"}:
            setattr(user, field, value)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user
