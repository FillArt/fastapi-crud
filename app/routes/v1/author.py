from typing import List
from fastapi import APIRouter, UploadFile, Depends, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas import AuthorOut, AuthorCreate, AuthorUpdate
from app.services.author import (
    get_author_all_service,
    get_author_service,
    create_author_service,
    delete_author_service,
    update_author_service,
    upload_author_photo_service,
    update_author_photo_service,
)

router = APIRouter()


@router.get("/", response_model=List[AuthorOut], tags=["Authors"])
async def get_all_author(db: AsyncSession = Depends(get_db)):
    return await get_author_all_service(db)

@router.get("/{id}", response_model=AuthorOut, tags=["Authors"])
async def get_author_by_id(id: int, db: AsyncSession = Depends(get_db)):
    return await get_author_service(db, id)

@router.post("/", response_model=AuthorOut, tags=["Authors"])
async def create_author(author: AuthorCreate, db: AsyncSession = Depends(get_db)):
    return await create_author_service(db, author)

@router.delete("/{id}", response_model=AuthorOut, tags=["Authors"])
async def delete_author(id: int, db: AsyncSession = Depends(get_db)):
    return await delete_author_service(db, id)

@router.patch("/{id}", response_model=AuthorOut, tags=["Authors"])
async def update_author(id: int, author: AuthorUpdate, db: AsyncSession = Depends(get_db)):
    return await update_author_service(db, id, author)

@router.post("/{id}/upload", response_model=AuthorOut, tags=["Authors"], summary="Upload avatar for author by ID")
async def upload_picture_by_id(id: int, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    return await upload_author_photo_service(db, id, file)

@router.patch("/{id}/upload", response_model=AuthorOut, tags=["Authors"], summary="Update avatar for author by ID")
async def update_picture_by_id(id: int, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    return await update_author_photo_service(db, id, file)
