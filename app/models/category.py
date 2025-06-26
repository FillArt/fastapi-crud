from sqlalchemy import Column, Integer, String
from app.db.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, autoincrement=False)
    name = Column(String, unique=True, index=True)