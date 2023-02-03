from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

import models
from controller import get_all_blog, get_all_blog_by_user, get_blog, store_blog, update_blog, destroy_blog, \
    store_blog_comment
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from auth import get_current_user, get_user_exception, login_for_access_token, create_new_user, UserSchema
from schemas import Blog, Comment

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
async def read_all(db: Session = Depends(get_db)):
    return await get_all_blog(db)


@app.get("/blogs/user")
async def read_all_by_user(user: dict = Depends(get_current_user),
                           db: Session = Depends(get_db)):
    return await get_all_blog_by_user(user, db)


@app.get("/blog/{blog_id}")
async def read_blog(blog_id: int, db: Session = Depends(get_db)):
    return await get_blog(blog_id, db)


@app.post("/blog")
async def create_blog(blog: Blog,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    return await store_blog(blog, user, db)


@app.put("/blog/{blog_id}")
async def change_blog(blog_id: int,
                      blog: Blog,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    return await update_blog(blog_id, blog, user, db)


@app.delete("/blog/{blog_id}")
async def delete_blog(blog_id: int,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    return await destroy_blog(blog_id, user, db)


@app.post("/blog/{blog_id}")
async def create_blog_comment(blog_id: int,comment: Comment,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    return await store_blog_comment(blog_id,comment, user, db)

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    return await login_for_access_token(form_data,db)

@app.post("/registration")
async def registration(user_data: UserSchema, db: Session = Depends(get_db)):
    return await create_new_user(user_data,db)
