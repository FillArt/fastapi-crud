from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.models.post_categories import post_categories


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String)
    categories = relationship("Category", secondary="post_categories", back_populates="posts")
    is_published = Column(Boolean, default=False, nullable=False)
    image_path = Column(String)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


