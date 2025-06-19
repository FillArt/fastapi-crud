from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.services.contact import contact_create, get_all_contacts
from app.schemas import ContactCreate
from app.db.database import get_db

router = APIRouter()

@router.post("/", response_model=ContactCreate, tags=["Contact"], summary="Sending data from a form to the server")
async def contact_send_data(request: ContactCreate, db: Session = Depends(get_db)):
    return contact_create(db, request)

@router.get("/", response_model=List[ContactCreate], tags=["Contact"], summary="Getting all contacts (for debugging)")
async def all_contacts(db: Session = Depends(get_db)):
    contacts = get_all_contacts(db)
    if contacts is None:
        raise HTTPException(status_code=404, detail="No contacts found")
    return contacts

# @router.post("/upload")
# async def upload_contact_file(request: ContactCreate, db: Session = Depends(get_db)):