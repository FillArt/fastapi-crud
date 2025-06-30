from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, Query, File
from fastapi_pagination import paginate, Page
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.posts import PostCreate, PostOut, PostUpdate, PostContentStatus
from app.services.posts import (
    get_posts_service,
    create_post_service,
    get_post_service,
    delete_post_service,
    update_post_service,
    picture_upload_service,
    change_status_service,
    update_picture_post_service,
    get_filtered_posts_service,
)

router = APIRouter()


@router.get("/", response_model=Page[PostOut], tags=["Posts"], summary="Get all posts")
async def get_paginated_posts(
    db: AsyncSession = Depends(get_db),
    category_id: Optional[int] = Query(None),
):
    posts = await get_filtered_posts_service(db, category_id)
    return paginate(posts)


@router.post("/", response_model=PostOut, tags=["Posts"], summary="Create a new post")
async def create_new_post(post: PostCreate, db: AsyncSession = Depends(get_db)):
    return await create_post_service(db, post)


@router.get("/{id}", response_model=PostOut, tags=["Posts"], summary="Get post by ID")
async def read_post(id: int, db: AsyncSession = Depends(get_db)):
    return await get_post_service(db, id)


@router.post("/{id}/upload", response_model=PostOut, tags=["Posts"], summary="Upload picture for post by ID")
async def upload_picture_by_id(id: int, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    return await picture_upload_service(db, id, file)


@router.delete("/{id}", tags=["Posts"], summary="Delete a post by ID")
async def delete_post_by_id(id: int, db: AsyncSession = Depends(get_db)):
    return await delete_post_service(db, id)


@router.patch("/{id}", response_model=PostOut, tags=["Posts"], summary="Update a post by ID")
async def update_post_by_id(id: int, post: PostUpdate, db: AsyncSession = Depends(get_db)):
    return await update_post_service(db, id, post)


@router.patch("/{id}/publish", response_model=PostOut, tags=["Posts"], summary="Update status post by ID")
async def update_status_by_id(id: int, post: PostContentStatus, db: AsyncSession = Depends(get_db)):
    return await change_status_service(db, id, post)


@router.patch("/{id}/upload", response_model=PostOut, tags=["Posts"], summary="Update picture for post by ID")
async def update_picture_by_id(id: int, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    return await update_picture_post_service(db, id, file)
