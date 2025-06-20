from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.models.association import post_category

class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String, unique=True, index=True)

    posts = relationship("Post", secondary=post_category, back_populates="categories")