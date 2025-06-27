import os
from uuid import uuid4

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.models import Author
from app.schemas import AuthorCreate, AuthorUpdate

def create_author_service(db: Session, author: AuthorCreate):
    db_author = Author(
        name=author.name,
        last_name=author.last_name,
        middle_name=author.middle_name,
        profession=author.profession,
    )

    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def get_author_service(db: Session, author_id: int):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author

def get_author_all_service(db: Session):
    return db.query(Author).all()

def delete_author_service(db: Session, author_id: int):
    author_queryset = db.query(Author).filter(Author.id == author_id).first()

    if not author_queryset:
        raise HTTPException(status_code=404, detail="Author not found")

    avatar_path = author_queryset.avatar_path
    if avatar_path:
        avatar_full_path = os.path.join(os.getcwd(), avatar_path)
        if os.path.exists(avatar_full_path):
            os.remove(avatar_full_path)

    db.delete(author_queryset)
    db.commit()

    return author_queryset

def update_author_service(db: Session, id: int, data: AuthorUpdate):
    author_queryset = db.query(Author).filter(Author.id == id).first()

    if not author_queryset:
        raise HTTPException(status_code=404, detail="Author not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(author_queryset, key, value)

    db.commit()
    db.refresh(author_queryset)
    return author_queryset


async def upload_author_photo_service(db: Session, id: int, file: UploadFile):
    author_queryset = db.query(Author).filter(Author.id == id).first()

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
    db.commit()
    db.refresh(author_queryset)
    return author_queryset

async def update_author_photo_service(db: Session, id: int, file: UploadFile):
    author_queryset = db.query(Author).filter(Author.id == id).first()

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
    db.commit()
    db.refresh(author_queryset)

    return author_queryset