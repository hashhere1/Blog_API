from fastapi import APIRouter, HTTPException, status
from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi import Depends

import models
import schemas
from database import get_db
from auth.hashing import verify
from auth.auth_token import create_access_token

router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login",response_model=schemas.Token)
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials"
        )
    if not verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Password"
        )
    access_token = create_access_token(
        data={"sub": user.email},
            expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token,
            "token_type": "Bearer"
            }