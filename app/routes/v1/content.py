from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.content import (
    PostContentOut, PostContentCreate, MessageResponse, PostContentUpdate
)
from app.services.content import (
    create_content_service,
    get_content_service,
    get_content_one_service,
    delete_content_service,
    delete_all_post_content_service,
    update_content_service
)

router = APIRouter()


@router.post("/{post_id}", response_model=PostContentOut, tags=["Content"], summary="Create a new content for post")
async def create_content_for_post(
    post_id: int = Path(..., description="ID поста"),
    content: PostContentCreate = Body(...),
    db: AsyncSession = Depends(get_db)
):
    return await create_content_service(db, post_id, content)


@router.get("/{post_id}", response_model=List[PostContentOut], tags=["Content"], summary="Get all content by ID post")
async def get_content_for_post(post_id: int, db: AsyncSession = Depends(get_db)):
    return await get_content_service(db, post_id)


@router.get("/{post_id}/{content_id}", response_model=PostContentOut, tags=["Content"], summary="Get content by ID")
async def get_content_by_content_id(post_id: int, content_id: int, db: AsyncSession = Depends(get_db)):
    return await get_content_one_service(db, content_id)


@router.delete("/{post_id}/{content_id}", response_model=PostContentOut, tags=["Content"], summary="Delete content by ID")
async def delete_content_for_post(post_id: int, content_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_content_service(db, content_id)


@router.delete("/{post_id}", response_model=MessageResponse, tags=["Content"], summary="Delete all content for post")
async def delete_all_content_for_post(post_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_all_post_content_service(db, post_id)


@router.patch("/{post_id}/{content_id}", response_model=PostContentOut, tags=["Content"], summary="Update content by ID")
async def update_content_for_post(
    post_id: int,
    content_id: int,
    data: PostContentUpdate,
    db: AsyncSession = Depends(get_db)
):
    return await update_content_service(db, content_id, data)
