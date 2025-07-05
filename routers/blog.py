from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from repository import blog
import schemas
from database import get_db
from auth.oauth2 import get_current_user

router = APIRouter(
    tags=["Blogs"]
)


@router.get("/blogs", response_model=List[schemas.ShowBlog])
def all_blogs(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return blog.all_blogs(db)


@router.post("/blog", status_code=201)
def create(request: schemas.Blog, db: Session = Depends(get_db),
           current_user: schemas.User = Depends(get_current_user)):
    return blog.create(request, db)


@router.get("/get_blog/{blog_id}", response_model=schemas.ShowBlog)
def get_blog(blog_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return blog.show_by_id(blog_id, db)


@router.delete("/delete_blog/{blog_id}")
def delete_blog(blog_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return blog.delete(blog_id, db)


@router.put("/update_blog/{id}")
def update(id: int, request: schemas.CreateBlog, db: Session = Depends(get_db),
           current_user: schemas.User = Depends(get_current_user)):
    return blog.update(id, request, db)
