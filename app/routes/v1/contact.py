from typing import List

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession  # <- async

from app.db.database import get_db
from app.schemas.contact import ContactCreate, ContactRead
from app.services.contact import contact_create_service, get_all_contacts_service, contact_upload_service, \
    get_by_id_service

router = APIRouter()

@router.post("/", response_model=ContactRead, tags=["Contact"], summary="Sending data from a form to the server")
async def contact_send_data(request: ContactCreate, db: AsyncSession = Depends(get_db)):
    return await contact_create_service(db, request)  # await!

@router.get("/", response_model=List[ContactRead], tags=["Contact"], summary="Getting all contacts (for debugging)")
async def all_contacts(db: AsyncSession = Depends(get_db)):
    return await get_all_contacts_service(db)  # await!

@router.get("/{id}", response_model=ContactRead, tags=["Contact"], summary="Getting a specific contact")
async def contact_by_id(id: int, db: AsyncSession = Depends(get_db)):
    return await get_by_id_service(id, db)  # await!

@router.post("/{id}/upload")
async def upload_contact_file(id: int,
                              file: UploadFile = File(...),
                              db: AsyncSession = Depends(get_db)):
    return await contact_upload_service(db, id, file)  # await!