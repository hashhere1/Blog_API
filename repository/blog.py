from sqlalchemy.orm import Session
import models
from fastapi import HTTPException, status


def all_blogs(db: Session):
    blogs = db.query(models.Blog).all()
    if not blogs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No blog found"
        )
    return blogs


def create(request, db: Session):
    user = db.query(models.User).filter(models.User.id == request.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id '{request.user_id}' not found, Create a user first!"
        )
    new_blog = models.Blog(title=request.title, body=request.body, user_id=request.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def show_by_id(blog_id: int, db: Session):
    blog_by_id = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog_by_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id '{blog_id}' not found"
        )
    return blog_by_id


def delete(blog_id: int, db: Session):
    destroy_blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not destroy_blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {blog_id} not found"
        )
    db.delete(destroy_blog)
    db.commit()
    return destroy_blog


def update(id: int, request, db: Session):
    update_blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not update_blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The blog with id '{id}' not found"
        )
    update_blog.title = request.title
    update_blog.body = request.body
    db.commit()
    db.refresh(update_blog)
    return update_blog
