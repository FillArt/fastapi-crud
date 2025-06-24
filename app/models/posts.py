from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB, ARRAY

from datetime import datetime, timezone

from app.db.database import Base


class Post(Base):
    __tablename__ = "posts"

    pk_id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String)
    categories=Column(ARRAY(Integer))

    # contentBlocks = Column(JSONB)
    image_path = Column(String)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))