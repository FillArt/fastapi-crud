import os
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Author
from app.schemas import AuthorCreate, AuthorUpdate


async def create_author_service(db: AsyncSession, author: AuthorCreate):
    db_author = Author(**author.dict())
    db.add(db_author)
    await db.commit()
    await db.refresh(db_author)
    return db_author


async def get_author_service(db: AsyncSession, author_id: int):
    result = await db.execute(select(Author).where(Author.id == author_id))
    db_author = result.scalar_one_or_none()
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


async def get_author_all_service(db: AsyncSession):
    result = await db.execute(select(Author))
    return result.scalars().all()


async def delete_author_service(db: AsyncSession, author_id: int):
    result = await db.execute(select(Author).where(Author.id == author_id))
    author_queryset = result.scalar_one_or_none()

    if not author_queryset:
        raise HTTPException(status_code=404, detail="Author not found")

    avatar_path = author_queryset.avatar_path
    if avatar_path:
        avatar_full_path = os.path.join(os.getcwd(), avatar_path)
        if os.path.exists(avatar_full_path):
            os.remove(avatar_full_path)

    await db.delete(author_queryset)
    await db.commit()
    return author_queryset


async def update_author_service(db: AsyncSession, id: int, data: AuthorUpdate):
    result = await db.execute(select(Author).where(Author.id == id))
    author_queryset = result.scalar_one_or_none()

    if not author_queryset:
        raise HTTPException(status_code=404, detail="Author not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(author_queryset, key, value)

    await db.commit()
    await db.refresh(author_queryset)
    return author_queryset


async def upload_author_photo_service(db: AsyncSession, id: int, file: UploadFile):
    result = await db.execute(select(Author).where(Author.id == id))
    author_queryset = result.scalar_one_or_none()

    if not author_queryset:
        raise HTTPException(status_code=404, detail="Author not found")

    static_dir = os.path.join(os.getcwd(), "static/author")
    os.makedirs(static_dir, exist_ok=True)

    ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid4().hex}{ext}"
    full_path = os.path.join(static_dir, unique_filename)
    relative_path = f"static/author/{unique_filename}"

    with open(full_path, "wb") as f:
        f.write(await file.read())

    author_queryset.avatar_path = relative_path
    await db.commit()
    await db.refresh(author_queryset)
    return author_queryset


async def update_author_photo_service(db: AsyncSession, id: int, file: UploadFile):
    result = await db.execute(select(Author).where(Author.id == id))
    author_queryset = result.scalar_one_or_none()

    if not author_queryset:
        raise HTTPException(status_code=404, detail="Author not found")

    # Remove old avatar
    if author_queryset.avatar_path:
        old_avatar_path = os.path.join(os.getcwd(), author_queryset.avatar_path)
        if os.path.isfile(old_avatar_path):
            try:
                os.remove(old_avatar_path)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to delete old avatar: {str(e)}")

    # Upload new avatar
    static_dir = os.path.join(os.getcwd(), "static/author")
    os.makedirs(static_dir, exist_ok=True)

    ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid4().hex}{ext}"
    full_path = os.path.join(static_dir, unique_filename)
    relative_path = f"static/author/{unique_filename}"

    with open(full_path, "wb") as f:
        f.write(await file.read())

    author_queryset.avatar_path = relative_path
    await db.commit()
    await db.refresh(author_queryset)
    return author_queryset
