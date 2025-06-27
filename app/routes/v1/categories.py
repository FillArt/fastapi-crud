from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.category import CategoryOut, CategoryCreate, CategoryWithCount, CategoryUpdate
from app.services.categories import get_all_service, delete_category_service, get_post_ids_by_category_service, \
    update_category_service, create_category_service, get_categories_with_post_count

router = APIRouter()


@router.post("/", response_model=CategoryOut, tags=["Categories"])
async def create_category_post(category: CategoryCreate, db: Session = Depends(get_db)):
    return create_category_service(db, category)


@router.get("/", response_model=List[CategoryWithCount], tags=["Categories"])
async def get_all_categories(db: Session = Depends(get_db)):
    return get_categories_with_post_count(db)


@router.delete("/{id}", response_model=CategoryOut, tags=["Categories"])
def delete_category_post(id: int, db: Session = Depends(get_db)):
    return delete_category_service(db, id)


@router.get("/{id}", response_model=List[int], tags=["Categories"])
def get_post_ids_by_category_route(id: int, db: Session = Depends(get_db)):
    return get_post_ids_by_category_service(db, id)


@router.patch("/{id}", response_model=CategoryOut, tags=["Categories"])
def update_category_by_id(id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    return update_category_service(db, id, category)
