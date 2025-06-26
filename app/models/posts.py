from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import ARRAY

from app.db.database import Base


class Post(Base):
    __tablename__ = "posts"

    pk_id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String)
    categories=Column(ARRAY(Integer))
    is_published = Column(Boolean, default=False, nullable=False)
    image_path = Column(String)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


