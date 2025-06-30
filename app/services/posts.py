import os
from typing import Optional
from uuid import uuid4

from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import Post, Category
from app.models.author import Author
from app.schemas.posts import PostCreate, PostUpdate, PostContentStatus
from app.services.content import delete_all_post_content_service


async def get_posts_service(db: AsyncSession):
    query = select(Post).options(selectinload(Post.categories))
    result = await db.execute(query)
    return result.scalars().all()


async def get_filtered_posts_service(db: AsyncSession, category_id: Optional[int] = None):
    if category_id and category_id != 0:
        query = (
            select(Post)
            .options(selectinload(Post.categories))
            .join(Post.categories)
            .filter(Category.id == category_id)
        )
    else:
        query = select(Post).options(selectinload(Post.categories))

    result = await db.execute(query)
    return result.scalars().all()


async def create_post_service(db: AsyncSession, data: PostCreate):
    result = await db.execute(select(Author).filter(Author.id == data.author_id))
    author = result.scalar_one_or_none()
    if not author:
        raise HTTPException(status_code=404, detail="Автор не найден")

    post_instance = Post(
        title=data.title,
        description=data.description,
        image_path=getattr(data, "image_path", None),
        author_id=data.author_id,
    )

    if data.categories:
        result = await db.execute(select(Category).filter(Category.id.in_(data.categories)))
        categories = result.scalars().all()

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
    await db.commit()
    await db.refresh(post_instance)

    # Грузим связи categories для корректной сериализации
    await db.refresh(post_instance, attribute_names=["categories"])
    return post_instance


async def get_post_service(db: AsyncSession, post_id: int):
    query = select(Post).options(selectinload(Post.categories)).filter(Post.id == post_id)
    result = await db.execute(query)
    post = result.scalar_one_or_none()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


async def update_post_service(db: AsyncSession, post_id: int, data: PostUpdate):
    query = select(Post).options(selectinload(Post.categories)).filter(Post.id == post_id)
    result = await db.execute(query)
    post_instance = result.scalar_one_or_none()

    if not post_instance:
        raise HTTPException(status_code=404, detail="Post not found")

    update_data = data.model_dump(exclude_unset=True)

    # Обработка categories отдельно
    if "categories" in update_data:
        category_ids = update_data.pop("categories")
        result = await db.execute(select(Category).filter(Category.id.in_(category_ids)))
        categories = result.scalars().all()

        found_ids = {cat.id for cat in categories}
        missing_ids = set(category_ids) - found_ids
        if missing_ids:
            raise HTTPException(
                status_code=404,
                detail=f"Category with id {list(missing_ids)} not found"
            )

        post_instance.categories = categories  # ← уже ORM объекты

    # Обновляем оставшиеся поля
    for key, value in update_data.items():
        setattr(post_instance, key, value)

    await db.commit()
    await db.refresh(post_instance, attribute_names=["categories"])
    return post_instance



async def delete_post_service(db: AsyncSession, post_id: int):
    query = select(Post).filter(Post.id == post_id)
    result = await db.execute(query)
    post_queryset = result.scalar_one_or_none()
    if post_queryset is None:
        raise HTTPException(status_code=404, detail="Post not found")

    if post_queryset.image_path:
        image_full_path = os.path.join(os.getcwd(), post_queryset.image_path)
        if os.path.exists(image_full_path):
            try:
                os.remove(image_full_path)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to delete image: {str(e)}")

    await delete_all_post_content_service(db, post_id)

    await db.delete(post_queryset)
    await db.commit()
    return post_queryset


async def picture_upload_service(db: AsyncSession, post_id: int, file: UploadFile):
    query = select(Post).filter(Post.id == post_id)
    result = await db.execute(query)
    post = result.scalar_one_or_none()
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
    await db.commit()
    await db.refresh(post)

    await db.refresh(post, attribute_names=["categories"])
    return post


async def change_status_service(db: AsyncSession, post_id: int, data: PostContentStatus):
    query = select(Post).filter(Post.id == post_id)
    result = await db.execute(query)
    post_instance = result.scalar_one_or_none()

    if not post_instance:
        raise HTTPException(status_code=404, detail="Post not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(post_instance, key, value)

    await db.commit()
    await db.refresh(post_instance, attribute_names=["categories"])
    return post_instance


async def update_picture_post_service(db: AsyncSession, post_id: int, file: UploadFile):
    query = select(Post).filter(Post.id == post_id)
    result = await db.execute(query)
    post = result.scalar_one_or_none()

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
    await db.commit()
    await db.refresh(post, attribute_names=["categories"])

    return post
