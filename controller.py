from fastapi import FastAPI, Depends, HTTPException
import models
from sqlalchemy.orm import Session

from auth import get_current_user, get_user_exception
from database import SessionLocal


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()



async def get_all_blog(db):
    return db.query(models.Blogs).all()

async def get_blog(blog_id: int,
                    db: Session = Depends(get_db)):

    blog_model = db.query(models.Blogs)\
        .filter(models.Blogs.id == blog_id)\
        .first()
    if blog_model is not None:
        comments = await get_all_comment_by_blog(db,blog_id)
        blog_model.comment = comments
        return blog_model
    raise http_exception()

async def store_blog(blog,user,db):
    if user is None:
        raise get_user_exception()
    blog_model = models.Blogs()
    blog_model.title = blog.title
    blog_model.description = blog.description
    blog_model.user_id = user.get("id")

    db.add(blog_model)
    db.commit()

    return successful_response(201)

async def update_blog(blog_id,blog,user,db):
    if user is None:
        raise get_user_exception()

    blog_model = db.query(models.Blogs) \
        .filter(models.Blogs.id == blog_id) \
        .filter(models.Blogs.user_id == user.get("id")) \
        .first()

    if blog_model is None:
        raise http_exception()

    blog_model.title = blog.title
    blog_model.description = blog.description
    blog_model.status = blog.status

    db.add(blog_model)
    db.commit()

    return successful_response(200)

async def destroy_blog(blog_id,user,db):
    if user is None:
        raise get_user_exception()

    blog_model = db.query(models.Blogs) \
        .filter(models.Blogs.id == blog_id) \
        .filter(models.Blogs.user_id == user.get("id")) \
        .first()

    if blog_model is None:
        raise http_exception()

    db.query(models.Blogs) \
        .filter(models.Blogs.id == blog_id) \
        .delete()
    db.query(models.Comments).filter(models.Comments.blog_id == blog_id) \
        .delete()

    db.commit()

    return successful_response(200)

async def get_all_blog_by_user(user,db):
    if user is None:
        raise get_user_exception()
    return db.query(models.Blogs)\
        .filter(models.Blogs.user_id == user.get("id"))\
        .all()



async def get_all_comment_by_blog(db,blog_id):
    return db.query(models.Comments)\
        .filter(models.Comments.blog_id == blog_id)\
        .all()

async def store_blog_comment(blog_id,comment,user,db):
    if user is None:
        raise get_user_exception()

    blog_model = db.query(models.Blogs) \
        .filter(models.Blogs.id == blog_id) \
        .first()
    if blog_model is None:
        raise http_exception()

    comment_model = models.Comments()
    comment_model.description = comment.description
    comment_model.user_id = user.get("id")
    comment_model.blog_id = blog_id

    db.add(comment_model)
    db.commit()

    return successful_response(201)


def successful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }


def http_exception():
    return HTTPException(status_code=404, detail="Blog not found")