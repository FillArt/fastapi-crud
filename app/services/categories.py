from fastapi import HTTPException

from app.schemas.category import CategoryCreate, CategoryOut
from app.models import Category
from sqlalchemy.orm import Session

def create_category(db: Session, category: CategoryCreate):
    existing = db.query(Category).filter(Category.name == category.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")

    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category