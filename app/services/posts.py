from fastapi import HTTPException
from app.db.fake_db import posts
from app.schemas.posts import PostBase

from app.models import Post
from sqlalchemy.orm import Session


def get_posts(db: Session):
    return db.query(Post).all()

def create_post(db: Session, data: PostBase):
    post_instance = Post(**data.model_dump())
    db.add(post_instance)
    db.commit()
    db.refresh(post_instance)
    return post_instance

def get_post(db: Session, id: int):
    return db.query(Post).filter(Post.id == id).first()

def update_post(db: Session, id: int, data: PostBase):
    post_queryset = db.query(Post).filter(Post.id == id).first()
    if post_queryset:
        for key, value in data.model_dump().items():
            setattr(post_queryset, key, value)
        db.commit()
        db.refresh(post_queryset)
    return post_queryset

def delete_post(db: Session, id: int):
    post_queryset = db.query(Post).filter(Post.id == id).first()
    if post_queryset:
        db.delete(post_queryset)
        db.commit()
    return post_queryset
