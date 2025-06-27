import os
from typing import Optional
from uuid import uuid4

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.models import Post, Category
from app.models.author import Author
from app.schemas.posts import PostCreate, PostUpdate, PostContentStatus
from app.services.content import delete_all_post_content_service


def get_posts_service(db: Session):
    return db.query(Post).all()

def get_filtered_posts_service(db: Session, category_id: Optional[int] = None):
    query = db.query(Post)

    if category_id and category_id != 0:
        query = query.join(Post.categories).filter(Category.id == category_id)

    return query.all()

def create_post_service(db: Session, data: PostCreate):
    author = db.query(Author).filter(Author.id == data.author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Автор не найден")

    post_instance = Post(
        title=data.title,
        description=data.description,
        image_path=getattr(data, "image_path", None),
        author_id=data.author_id
    )

    if data.categories:
        categories = db.query(Category).filter(Category.id.in_(data.categories)).all()

        found_ids = {cat.id for cat in categories}
        requested_ids = set(data.categories)

        missing_ids = requested_ids - found_ids
        if missing_ids:
            raise HTTPException(
                status_code=404,
                detail=f"Category with id {list(missing_ids)} not found!."
            )

        post_instance.categories = categories

    db.add(post_instance)
    db.commit()
    db.refresh(post_instance)
    return post_instance


def get_post_service(db: Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

def update_post_service(db: Session, post_id: int, data: PostUpdate):
    post_instance = db.query(Post).filter(Post.id == post_id).first()
    if not post_instance:
        raise HTTPException(status_code=404, detail="Post not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(post_instance, key, value)

    db.commit()
    db.refresh(post_instance)
    return post_instance

def delete_post_service(db: Session, post_id: int):
    post_queryset = db.query(Post).filter(Post.id == post_id).first()
    if post_queryset is None:
        raise HTTPException(status_code=404, detail="Post not found")

    if post_queryset.image_path:
        image_full_path = os.path.join(os.getcwd(), post_queryset.image_path)
        if os.path.exists(image_full_path):
            try:
                os.remove(image_full_path)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to delete image: {str(e)}")

    if post_queryset:
        delete_all_post_content_service(db, post_id)
        db.delete(post_queryset)
        db.commit()
    return post_queryset


async def picture_upload_service(db: Session, post_id: int, file: UploadFile):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    static_dir = os.path.join(os.getcwd(), "static/blog")
    os.makedirs(static_dir, exist_ok=True)

    ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid4().hex}{ext}"

    full_path = os.path.join(static_dir, unique_filename)
    relative_path = f"static/blog/{unique_filename}"

    with open(full_path, "wb") as f:
        f.write(await file.read())

    post.image_path = relative_path
    db.commit()
    db.refresh(post)

    return post

def change_status_service(db: Session, post_id: int, data: PostContentStatus):
    post_instance = db.query(Post).filter(Post.id == post_id).first()

    if not post_instance:
        raise HTTPException(status_code=404, detail="Post not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(post_instance, key, value)

    db.commit()
    db.refresh(post_instance)
    return post_instance


async def update_picture_post_service(db: Session, post_id: int, file: UploadFile):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.image_path:
        old_avatar_path = os.path.join(os.getcwd(), post.image_path)
        if os.path.isfile(old_avatar_path):
            try:
                os.remove(old_avatar_path)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to delete old avatar: {str(e)}")

    static_dir = os.path.join(os.getcwd(), "static/blog")
    os.makedirs(static_dir, exist_ok=True)

    ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid4().hex}{ext}"
    full_path = os.path.join(static_dir, unique_filename)
    relative_path = f"static/blog/{unique_filename}"

    with open(full_path, "wb") as f:
        f.write(await file.read())

    post.image_path = relative_path
    db.commit()
    db.refresh(post)

    return post
