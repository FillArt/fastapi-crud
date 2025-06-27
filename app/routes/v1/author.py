from typing import List

from fastapi import APIRouter, UploadFile
from fastapi.params import Depends, File
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas import AuthorOut, AuthorCreate, AuthorUpdate
from app.services.author import get_author_all_service, get_author_service, create_author_service, \
    delete_author_service, update_author_service, upload_author_photo_service

router = APIRouter()


@router.get("/author", response_model=List[AuthorOut], tags=["Authors"])
def get_all_author(db: Session = Depends(get_db)):
    return get_author_all_service(db)

@router.get("/author/{id}", response_model=AuthorOut, tags=["Authors"])
def get_author_by_id(id: int, db: Session = Depends(get_db)):
    return get_author_service(db, id)

@router.post('/author', response_model=AuthorOut, tags=["Authors"])
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    return create_author_service(db, author)

@router.delete("/author/{id}", response_model=AuthorOut, tags=["Authors"])
def delete_author(id: int, db: Session = Depends(get_db)):
    return delete_author_service(db, id)

@router.patch("/author/{id}", response_model=AuthorOut, tags=["Authors"])
def update_author(id: int, author: AuthorUpdate, db: Session = Depends(get_db)):
    return update_author_service(db, id, author)

@router.post("/{id}/upload", response_model=AuthorOut, tags=["Authors"], summary="Upload avatar for author by ID")
async def upload_picture_by_id(id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    return await upload_author_photo_service(db, id, file)