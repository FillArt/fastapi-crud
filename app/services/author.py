from fastapi import HTTPException
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

    db.delete(author_queryset)
    db.commit()
    db.refresh(author_queryset)
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

