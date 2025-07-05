from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
from auth.oauth2 import get_current_user
import schemas
from repository import user
from database import get_db

router = APIRouter(
    tags=["Users"]
)


@router.post("/create_user", response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request, db)


@router.get("/show_user/{id}", response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return user.show(id, db)


@router.get("/all_users", response_model=List[schemas.ShowUser])
def all_users(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return db.query(models.User).all()


@router.delete("/delete_user/{id}")
def delete(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return user.delete(id, db)
