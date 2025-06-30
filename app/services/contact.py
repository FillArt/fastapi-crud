from typing import List, Any, Coroutine, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import os
from uuid import uuid4

from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.models import Contact
from app.schemas.contact import ContactCreate
from fastapi import status


MAX_FILE_SIZE_MB = 5
MAX_FILE_SIZE = MAX_FILE_SIZE_MB * 1024 * 1024


async def contact_create_service(db: AsyncSession, request: ContactCreate)  -> Contact:
    contact_instance = Contact(**request.dict())
    db.add(contact_instance)
    await db.commit()
    await db.refresh(contact_instance)
    return contact_instance

async def get_all_contacts_service(db: AsyncSession) -> Sequence[Contact]:
    result = await db.execute(select(Contact))
    contacts = result.scalars().all()
    if not contacts:
        raise HTTPException(status_code=404, detail="No contacts found")
    return contacts

async def get_by_id_service(contact_id: int, db: AsyncSession) -> type[Contact]:
    contact = await db.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="No contact found")
    return contact


async def contact_upload_service(db: AsyncSession, contact_id: int, file: UploadFile) -> type[Contact]:
    contact = await db.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="No contacts found")

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Max size is {MAX_FILE_SIZE_MB}MB.",
        )

    os.makedirs("documents", exist_ok=True)
    ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid4().hex}{ext}"
    file_path = os.path.join("documents", unique_filename)

    # Записываем содержимое файла на диск
    with open(file_path, "wb") as f:
        f.write(contents)

    contact.file_path = file_path
    await db.commit()
    await db.refresh(contact)
    return contact



