from datetime import timedelta, datetime, timezone
from typing import Optional

from jose import jwt

SECRET_KEY = "7AlBaQQSuVfxYVeLyKX1G-4WfVc2PTdxE7BYQIUeSOYmxmRXpo4AqbfkFLLsjR7TZA_7p9Fu38raedB2pH31Og"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,ALGORITHM)
    return encoded_jwt
