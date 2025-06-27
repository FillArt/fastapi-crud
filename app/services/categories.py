from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


def create_category_service(db: Session, category: CategoryCreate):
    existing = db.query(Category).filter(Category.name == category.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")

    db_category = Category(
        name=category.name
    )

    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_all_service(db: Session):
    return db.query(Category).all()

def get_post_ids_by_category_service(db: Session, id: int):
    category = db.query(Category).filter(Category.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

def delete_category_service(db: Session, id: int):
    category_queryset = db.query(Category).filter(Category.id == id).first()

    if not category_queryset:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category_queryset)
    db.commit()
    return category_queryset

def update_category_service(db: Session, id: int, data: CategoryUpdate):
    category_queryset = db.query(Category).filter(Category.id == id).first()
    if not category_queryset:
        raise HTTPException(status_code=404, detail="Category not found")

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(category_queryset, key, value)

    db.commit()
    db.refresh(category_queryset)
    return category_queryset

