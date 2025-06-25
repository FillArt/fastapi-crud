import os
from uuid import uuid4

from fastapi import HTTPException, UploadFile

from app.models.posts import PostContent
from app.schemas.posts import PostBase, PostCreate, PostUpdate, PostContentCreate
from app.models import Post, Category
from sqlalchemy.orm import Session


def get_posts(db: Session):
    return db.query(Post).all()

def create_post(db: Session, data: PostCreate):
    post_instance = Post(
        title=data.title,
        description=data.description,
        image_path=getattr(data, "image_path", None),
        categories=data.categories or []
    )

    db.add(post_instance)
    db.commit()
    db.refresh(post_instance)
    return post_instance


def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.pk_id == post_id).first()


def update_post(db: Session, post_id: int, data: PostUpdate):
    post_instance = db.query(Post).filter(Post.pk_id == post_id).first()
    if not post_instance:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(post_instance, key, value)

    db.commit()
    db.refresh(post_instance)
    return post_instance

def delete_post(db: Session, post_id: int):
    post_queryset = db.query(Post).filter(Post.pk_id == post_id).first()
    if post_queryset:
        db.delete(post_queryset)
        db.commit()
    return post_queryset


async def picture_upload(db: Session, post_id: int, file: UploadFile):
    post = db.query(Post).filter(Post.pk_id == post_id).first()

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

def create_content(db: Session, post_id: int, content_data: PostContentCreate):
    post = db.query(Post).filter(Post.pk_id == post_id).first()
    if not post:
        return None

    new_content = PostContent(
        post_id=post_id,
        type=content_data.type,
        value=content_data.value.dict(),
        order=content_data.order,
    )

    db.add(new_content)
    db.commit()
    db.refresh(new_content)
    return new_content