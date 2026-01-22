from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.core.database import get_session
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.models.user import User
from app.schemas.user import UserCreate, Token


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
def register(
    data: UserCreate,
    session: Session = Depends(get_session)
):
    exists = session.exec(
        select(User).where(User.email == data.email)
    ).first()
    if exists:
        raise HTTPException(400, "Email already registered")

    user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        experience_level=data.experience_level,
        current_phase=data.current_phase,
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    token = create_access_token(subject=str(user.id))
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    user = session.exec(
        select(User).where(User.email == form.username)
    ).first()

    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token(subject=str(user.id))
    return {"access_token": token, "token_type": "bearer"}
