import enum
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB

from app.db.database import Base

class ContentType(str, enum.Enum):
    text = "text"
    title = "title"
    quote = "quote"
    image = "image"
    list = "list"

class PostContent(Base):
    __tablename__ = "post_content"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    type = Column(SqlEnum(ContentType, name="content_type_enum"), nullable=False)
    value = Column(JSONB, nullable=False)
    order = Column(Integer, nullable=False)