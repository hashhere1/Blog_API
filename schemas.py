from pydantic import BaseModel
from typing import Optional


class Blog(BaseModel):
    title: str
    body: str
    user_id: int


class CreateBlog(Blog):
    pass


class ShowUser(BaseModel):
    name: str
    email: str


class ShowBlog(BaseModel):
    title: str
    body: str
    author: ShowUser

    class Config():
        orm_mode = True


class User(ShowUser):
    password: str

    class Config():
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
