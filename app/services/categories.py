from fastapi import HTTPException
from sqlalchemy import select

from app.schemas.category import CategoryCreate, CategoryOut
from app.models import Category, post_category, Post
from sqlalchemy.orm import Session

def create_category(db: Session, category: CategoryCreate):
    existing = db.query(Category).filter(Category.name == category.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")

    db_category = Category(
        category_id=category.category_id,
        name=category.name
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_all(db: Session):
    return db.query(Category).all()

def get_post_ids_by_category(db: Session, category_id: int):
    stmt = (
        select(Post.id)
        .join(post_category, Post.id == post_category.c.post_id)
        .where(post_category.c.category_id == category_id)
    )
    post_ids = db.execute(stmt).scalars().all()
    return post_ids


def delete_category(db: Session, id: int):
    category_queryset = db.query(Category).filter(Category.category_id == id).first()

    if not category_queryset:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category_queryset)
    db.commit()
    return category_queryset