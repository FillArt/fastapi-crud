from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Category
from app.models.post_categories import post_categories
from app.schemas.category import CategoryCreate, CategoryUpdate


async def create_category_service(db: AsyncSession, category: CategoryCreate):
    result = await db.execute(select(Category).where(Category.name == category.name))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")

    db_category = Category(name=category.name)

    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


async def get_all_service(db: AsyncSession):
    result = await db.execute(select(Category))
    return result.scalars().all()


async def get_post_ids_by_category_service(db: AsyncSession, id: int):
    result = await db.execute(select(Category).where(Category.id == id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


async def delete_category_service(db: AsyncSession, id: int):
    result = await db.execute(select(Category).where(Category.id == id))
    category_queryset = result.scalar_one_or_none()
    if not category_queryset:
        raise HTTPException(status_code=404, detail="Category not found")

    await db.delete(category_queryset)
    await db.commit()
    return category_queryset


async def update_category_service(db: AsyncSession, id: int, data: CategoryUpdate):
    result = await db.execute(select(Category).where(Category.id == id))
    category_queryset = result.scalar_one_or_none()
    if not category_queryset:
        raise HTTPException(status_code=404, detail="Category not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(category_queryset, key, value)

    await db.commit()
    await db.refresh(category_queryset)
    return category_queryset


async def get_categories_with_post_count(db: AsyncSession):
    result = await db.execute(
        select(
            Category.id,
            Category.name,
            func.count(post_categories.c.post_id).label("post_count")
        )
        .outerjoin(post_categories, Category.id == post_categories.c.category_id)
        .group_by(Category.id)
    )

    return [
        {
            "id": row.id,
            "name": row.name,
            "post_count": row.post_count
        }
        for row in result.all()
    ]
