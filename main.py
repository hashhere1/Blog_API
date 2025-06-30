from fastapi import FastAPI, Depends, HTTPException, status
from typing import List
import schemas
from schemas import Blog
from database import engine, get_db
import models
import uvicorn
from sqlalchemy.orm import Session
from hashing import hashing

app = FastAPI()
models.Base.metadata.create_all(engine)


@app.post("/blog", status_code=201, tags=["blogs"])
def create(request: Blog, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == request.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id '{request.user_id}' not found"
        )
    new_blog = models.Blog(title=request.title, body=request.body,user_id = request.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/get_blog/{blog_id}", response_model=schemas.ShowBlog, tags=["blogs"])
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    blog_by_id = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog_by_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id '{blog_id}' not found"
        )
    return blog_by_id


@app.get("/blogs", response_model=List[schemas.ShowBlog], tags=["blogs"])
def all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    if not blogs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No blog found"
        )
    return blogs


@app.delete("/delete_blog/{blog_id}", tags=["blogs"])
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    destroy_blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not destroy_blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {blog_id} not found"
        )
    db.delete(destroy_blog)
    db.commit()
    return destroy_blog


@app.put("/update_blog/{id}", tags=["blogs"])
def update(id: int, request: schemas.CreateBlog, db: Session = Depends(get_db)):
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


@app.post("/create_user", response_model=schemas.ShowUser, tags=["users"])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=hashing(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/show_user/{id}", response_model=schemas.ShowUser, tags=["users"])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id '{id}' not found"
        )
    return user


@app.get("/all_users", response_model=List[schemas.ShowUser], tags=["users"])
def all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@app.delete("/delete_user/{id}", tags=["users"])
def delete(id: int, db: Session = Depends(get_db)):
    delete_user = db.query(models.User).filter(models.User.id == id).first()
    if not delete_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with id '{id}' not found"
        )
    db.delete(delete_user)
    db.commit()
    return {"Result": f"The user with id '{id}' is deleted"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
