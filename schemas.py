from typing import Optional
from pydantic import BaseModel, Field

import models
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Todo(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6, description="The priority must be between 1-5")
    complete: bool


class Blog(BaseModel):
    title: str
    description: Optional[str]
    status: bool

class Blog(BaseModel):
    title: str
    description: Optional[str]
    status: bool





class Blog(BaseModel):
    title: str
    description: Optional[str]
    status: bool | None=None


class Comment(BaseModel):
    description: str
