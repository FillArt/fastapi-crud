from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.category import CategoryOut, CategoryCreate, CategoryWithCount, CategoryUpdate
from app.services.categories import create_category, get_all, delete_category, get_post_ids_by_category, update_category

router = APIRouter()

@router.post("/", response_model=CategoryOut, tags=["Categories"])
async def create_category_post(category: CategoryCreate , db: Session = Depends(get_db)):
    return create_category(db, category)

@router.get("/", response_model=List[CategoryOut], tags=["Categories"])
async def get_all_categories(db: Session = Depends(get_db)):
    return get_all(db)

@router.delete("/{pk_id}", response_model=CategoryOut, tags=["Categories"])
def delete_category_post(pk_id: int, db: Session = Depends(get_db)):
    return  delete_category(db, pk_id)

@router.get("/{pk_id}", response_model=List[int], tags=["Categories"])
def get_post_ids_by_category_route(pk_id: int, db: Session = Depends(get_db)):
    return get_post_ids_by_category(db, pk_id)

@router.patch("/{pk_id}", response_model=CategoryOut, tags=["Categories"])
def update_category_by_id(pk_id: int, category: CategoryUpdate , db: Session = Depends(get_db)):
    return update_category(db, pk_id, category)
