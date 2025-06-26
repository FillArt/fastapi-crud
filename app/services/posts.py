import os
from uuid import uuid4

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.models import Post, Category
from app.schemas.posts import PostCreate, PostUpdate, PostContentStatus
from app.services.content import delete_all_post_content


def get_posts(db: Session):
    return db.query(Post).all()

def create_post(db: Session, data: PostCreate):
    post_instance = Post(
        title=data.title,
        description=data.description,
        image_path=getattr(data, "image_path", None),
    )

    if data.categories:
        post_instance.categories = db.query(Category).filter(Category.id.in_(data.categories)).all()

    db.add(post_instance)
    db.commit()
    db.refresh(post_instance)
    return post_instance


def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()


def update_post(db: Session, post_id: int, data: PostUpdate):
    post_instance = db.query(Post).filter(Post.id == post_id).first()
    if not post_instance:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(post_instance, key, value)

    db.commit()
    db.refresh(post_instance)
    return post_instance

def delete_post(db: Session, post_id: int):
    post_queryset = db.query(Post).filter(Post.id == post_id).first()
    if post_queryset:
        delete_all_post_content(db, post_id)
        db.delete(post_queryset)
        db.commit()
    return post_queryset


async def picture_upload(db: Session, post_id: int, file: UploadFile):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    static_dir = os.path.join(os.getcwd(), "static")
    os.makedirs(static_dir, exist_ok=True)

    ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid4().hex}{ext}"

    full_path = os.path.join(static_dir, unique_filename)
    relative_path = f"static/{unique_filename}"

    with open(full_path, "wb") as f:
        f.write(await file.read())

    post.image_path = relative_path
    db.commit()
    db.refresh(post)

    return post

def change_status(db: Session, post_id: int, data: PostContentStatus):
    post_instance = db.query(Post).filter(Post.id == post_id).first()

    if not post_instance:
        raise HTTPException(status_code=404, detail="Post not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(post_instance, key, value)

    db.commit()
    db.refresh(post_instance)
    return post_instance

