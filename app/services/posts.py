import os
from uuid import uuid4

from fastapi import HTTPException, UploadFile

from app.schemas.posts import PostBase, PostCreate
from app.models import Post, Category
from sqlalchemy.orm import Session


def get_posts(db: Session):
    return db.query(Post).all()

def create_post(db: Session, data: PostCreate):
    category_ids = data.category_ids

    categories = db.query(Category).filter(Category.category_id.in_(category_ids)).all()

    if len(categories) != len(set(category_ids)):
        raise HTTPException(status_code=400, detail="One or more categories not found")

    post_data = data.model_dump()
    post_data.pop("category_ids", None)

    post_instance = Post(
        title=post_data.get("title"),
        description=post_data.get("description"),
        content=post_data.get("content"),
    )

    post_instance.categories = categories

    db.add(post_instance)
    db.commit()
    db.refresh(post_instance)

    return post_instance

def get_post(db: Session, id: int):
    return db.query(Post).filter(Post.id == id).first()

def update_post(db: Session, id: int, data: PostBase):
    post_queryset = db.query(Post).filter(Post.id == id).first()
    if post_queryset:
        for key, value in data.model_dump().items():
            setattr(post_queryset, key, value)
        db.commit()
        db.refresh(post_queryset)
    return post_queryset

def delete_post(db: Session, id: int):
    post_queryset = db.query(Post).filter(Post.id == id).first()
    if post_queryset:
        db.delete(post_queryset)
        db.commit()
    return post_queryset


async def picture_upload(db: Session, post_id: int, file: UploadFile):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # создаем папку, если нет
    static_dir = os.path.join(os.getcwd(), "static")
    os.makedirs(static_dir, exist_ok=True)

    # генерируем уникальное имя файла
    ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid4().hex}{ext}"

    # абсолютный путь, чтобы сохранить файл
    full_path = os.path.join(static_dir, unique_filename)

    # относительный путь для image_path
    relative_path = f"static/{unique_filename}"

    # сохраняем файл
    with open(full_path, "wb") as f:
        f.write(await file.read())

    # сохраняем путь в БД
    post.image_path = relative_path
    db.commit()
    db.refresh(post)

    return post