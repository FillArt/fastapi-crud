from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.models.association import post_category


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String)
    content = Column(String)
    image_path = Column(String)

    categories = relationship("Category", secondary=post_category, back_populates="posts")