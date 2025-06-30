from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.category import (
    CategoryOut,
    CategoryCreate,
    CategoryWithCount,
    CategoryUpdate,
)
from app.services.categories import (
    get_all_service,
    delete_category_service,
    get_post_ids_by_category_service,
    update_category_service,
    create_category_service,
    get_categories_with_post_count,
)

router = APIRouter()

@router.post("/", response_model=CategoryOut, tags=["Categories"])
async def create_category_post(category: CategoryCreate, db: AsyncSession = Depends(get_db)):
    return await create_category_service(db, category)

@router.get("/", response_model=List[CategoryWithCount], tags=["Categories"])
async def get_all_categories(db: AsyncSession = Depends(get_db)):
    return await get_categories_with_post_count(db)

@router.delete("/{id}", response_model=CategoryOut, tags=["Categories"])
async def delete_category_post(id: int, db: AsyncSession = Depends(get_db)):
    return await delete_category_service(db, id)

@router.get("/{id}", response_model=List[int], tags=["Categories"])
async def get_post_ids_by_category_route(id: int, db: AsyncSession = Depends(get_db)):
    category = await get_post_ids_by_category_service(db, id)
    return [post.id for post in category.posts]  # если posts связан через relationship

@router.patch("/{id}", response_model=CategoryOut, tags=["Categories"])
async def update_category_by_id(id: int, category: CategoryUpdate, db: AsyncSession = Depends(get_db)):
    return await update_category_service(db, id, category)
