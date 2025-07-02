from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import models
from auth.hashing import hashing


def create(request, db: Session):
    new_user = models.User(name=request.name, email=request.email, password=hashing(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def show(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id '{id}' not found"
        )
    return user


def delete(id: int, db: Session):
    delete_user = db.query(models.User).filter(models.User.id == id).first()
    if not delete_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with id '{id}' not found"
        )
    db.delete(delete_user)
    db.commit()
    return {"Result": f"The user with id '{id}' is deleted"}
