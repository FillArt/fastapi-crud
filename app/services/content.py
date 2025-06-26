from sqlalchemy.orm import Session

from app.models import Post
from app.models.content import PostContent
from app.schemas.content import PostContentCreate, PostContentUpdate


def create_content(db: Session, post_id: int, content_data: PostContentCreate):
    post = db.query(Post).filter(Post.id == post_id).first()
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

def get_content(db: Session, post_id: int):
    return db.query(PostContent).filter(PostContent.post_id == post_id).all()

def get_content_one(db: Session, content_id: int):
    return db.query(PostContent).filter(PostContent.id == content_id).first()

def delete_all_post_content(db: Session, post_id: int):
    count = db.query(PostContent).filter(PostContent.post_id == post_id).delete(synchronize_session=False)
    if count == 0:
        return None

    db.commit()
    return {"detail": f"Deleted {count} content block(s)"}

def delete_content(db: Session, content_id: int):
    row = db.query(PostContent).filter(PostContent.id == content_id).first()
    if row is None:
        return None

    db.delete(row)
    db.commit()
    return row

def update_content(db: Session, content_id: int, data: PostContentUpdate):
    content_instance = db.query(PostContent).filter(PostContent.id == content_id).first()
    if not content_instance:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(content_instance, key, value)

    db.commit()
    db.refresh(content_instance)
    return content_instance