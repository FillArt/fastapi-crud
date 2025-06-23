from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from datetime import datetime, timezone

from app.db.database import Base
from app.models.association import post_category


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String)
    image_path = Column(String)

    content_blocks = Column(JSONB, nullable=False)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    categories = relationship("Category", secondary=post_category, back_populates="posts")