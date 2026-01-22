from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
from fastapi.security import OAuth2PasswordBearer

import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

from app.core.config import settings

password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)

# subject - user.id (string!)
def create_access_token(
    subject: str,
    expires_delta: Optional[timedelta] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload: Dict[str, Any] = {
        "sub": subject,
        "exp": datetime.now(timezone.utc) + expires_delta,
        "iat": datetime.now(timezone.utc),
        "type": "access",
    }

    if extra:
        payload.update(extra)

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
    except InvalidTokenError:
        raise
