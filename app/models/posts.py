import enum
from sqlalchemy import Enum as SqlEnum


from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, ARRAY

from datetime import datetime, timezone

from app.db.database import Base


class Post(Base):
    __tablename__ = "posts"

    pk_id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String)
    categories=Column(ARRAY(Integer))

    image_path = Column(String)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ContentType(str, enum.Enum):
    text = "text"
    title = "title"
    quote = "quote"
    image = "image"
    list = "list"

class PostContent(Base):
    __tablename__ = "post_content"

    pk_id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.pk_id"))
    type = Column(SqlEnum(ContentType, name="content_type_enum"), nullable=False)
    value = Column(JSONB, nullable=False)
    order = Column(Integer, nullable=False)
