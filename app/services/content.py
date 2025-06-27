from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Post
from app.models.content import PostContent
from app.schemas.content import PostContentCreate, PostContentUpdate


def create_content_service(db: Session, post_id: int, content_data: PostContentCreate):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

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

def get_content_service(db: Session, post_id: int):
    post_content = db.query(PostContent).filter(PostContent.post_id == post_id).all()
    if not post_content:
        raise HTTPException(status_code=404, detail="Content not found")
    return post_content

def get_content_one_service(db: Session, content_id: int):
    post_content = db.query(PostContent).filter(PostContent.id == content_id).first()
    if not post_content:
        raise HTTPException(status_code=404, detail="Content not found")
    return post_content

def delete_all_post_content_service(db: Session, post_id: int):
    count = db.query(PostContent).filter(PostContent.post_id == post_id).delete(synchronize_session=False)
    if count == 0:
        raise HTTPException(status_code=404, detail="No content found for this post")

    db.commit()
    return {"detail": f"Deleted {count} content block(s)"}

def delete_content_service(db: Session, content_id: int):
    row = db.query(PostContent).filter(PostContent.id == content_id).first()
    if row is None:
        raise HTTPException(status_code=404, detail="Content not found")

    db.delete(row)
    db.commit()
    return row

def update_content_service(db: Session, content_id: int, data: PostContentUpdate):
    content_instance = db.query(PostContent).filter(PostContent.id == content_id).first()
    if not content_instance:
        raise HTTPException(status_code=404, detail="Content not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(content_instance, key, value)

    db.commit()
    db.refresh(content_instance)
    return content_instance