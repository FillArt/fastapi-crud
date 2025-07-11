from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

from app.models.post_categories import post_categories


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)

    posts = relationship("Post", secondary="post_categories", back_populates="categories")
