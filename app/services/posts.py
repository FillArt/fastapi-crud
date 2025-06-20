from fastapi import HTTPException

from app.schemas.posts import PostBase, PostCreate
from app.models import Post, Category
from sqlalchemy.orm import Session


def get_posts(db: Session):
    return db.query(Post).all()

def create_post(db: Session, data: PostCreate):
    category_ids = data.category_ids

    categories = db.query(Category).filter(Category.category_id.in_(category_ids)).all()

    if len(categories) != len(set(category_ids)):
        raise HTTPException(status_code=400, detail="One or more categories not found")

    post_data = data.model_dump()
    post_data.pop("category_ids", None)

    post_instance = Post(
        title=post_data.get("title"),
        description=post_data.get("description"),
        content=post_data.get("content"),
    )

    post_instance.categories = categories

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
