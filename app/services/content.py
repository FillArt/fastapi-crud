from fastapi import HTTPException
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Post
from app.models.content import PostContent
from app.schemas.content import PostContentCreate, PostContentUpdate


async def create_content_service(db: AsyncSession, post_id: int, content_data: PostContentCreate):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_content = PostContent(
        post_id=post_id,
        type=content_data.type,
        value=content_data.value.dict(),
        order=content_data.order,
    )

    db.add(new_content)
    await db.commit()
    await db.refresh(new_content)
    return new_content


async def get_content_service(db: AsyncSession, post_id: int):
    result = await db.execute(select(PostContent).where(PostContent.post_id == post_id))
    return result.scalars().all()


async def get_content_one_service(db: AsyncSession, content_id: int):
    result = await db.execute(select(PostContent).where(PostContent.id == content_id))
    content = result.scalar_one_or_none()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content


async def delete_all_post_content_service(db: AsyncSession, post_id: int):
    stmt = delete(PostContent).where(PostContent.post_id == post_id)
    result = await db.execute(stmt)
    await db.commit()
    return {"detail": f"Deleted {result.rowcount} content block(s)"}


async def delete_content_service(db: AsyncSession, content_id: int):
    result = await db.execute(select(PostContent).where(PostContent.id == content_id))
    row = result.scalar_one_or_none()
    if row is None:
        raise HTTPException(status_code=404, detail="Content not found")

    await db.delete(row)
    await db.commit()
    return row


async def update_content_service(db: AsyncSession, content_id: int, data: PostContentUpdate):
    result = await db.execute(select(PostContent).where(PostContent.id == content_id))
    content_instance = result.scalar_one_or_none()
    if not content_instance:
        raise HTTPException(status_code=404, detail="Content not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(content_instance, key, value)

    await db.commit()
    await db.refresh(content_instance)
    return content_instance
