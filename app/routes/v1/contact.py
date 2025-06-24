from typing import List

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.contact import ContactCreate, ContactRead
from app.services.contact import contact_create, get_all_contacts, contact_upload, get_by_id

router = APIRouter()


@router.post("/", response_model=ContactRead, tags=["Contact"], summary="Sending data from a form to the server")
async def contact_send_data(request: ContactCreate, db: Session = Depends(get_db)):
    return contact_create(db, request)


@router.get("/", response_model=List[ContactRead], tags=["Contact"], summary="Getting all contacts (for debugging)")
async def all_contacts(db: Session = Depends(get_db)):
    contacts = get_all_contacts(db)
    if contacts is None:
        raise HTTPException(status_code=404, detail="No contacts found")
    return contacts

@router.get("/{id}", response_model=ContactRead, tags=["Contact"], summary="Getting a specific contact")
async def contact_by_id(id: int, db: Session = Depends(get_db)):
 contact = get_by_id(id, db)
 if contact is None:
     raise HTTPException(status_code=404, detail="No contact found")
 return contact

@router.post("/{id}/upload")
async def upload_contact_file(id: int,
                              file: UploadFile = File(...),
                              db: Session = Depends(get_db)):
    return await contact_upload(db, id, file)
