import os
from uuid import uuid4

from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.models import Contact
from app.schemas.contact import ContactCreate
from fastapi import status


MAX_FILE_SIZE_MB = 5
MAX_FILE_SIZE = MAX_FILE_SIZE_MB * 1024 * 1024


def contact_create(db: Session, request: ContactCreate):
    contact_instance = Contact(**request.dict())
    db.add(contact_instance)
    db.commit()
    db.refresh(contact_instance)
    return contact_instance

def get_all_contacts(db: Session):
    return db.query(Contact).all()


async def contact_upload(db: Session, contact_id: int, file: UploadFile):
    contact = db.get(Contact, contact_id)
    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Max size is {MAX_FILE_SIZE_MB}MB.",
        )


    if not contact:
        raise HTTPException(status_code=404, detail="No contacts found")

    os.makedirs("documents", exist_ok=True)
    ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid4().hex}{ext}"
    file_path = os.path.join("documents", unique_filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    contact.file_path = file_path
    db.commit()
    db.refresh(contact)
    return contact




