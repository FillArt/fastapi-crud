from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    profession = Column(String, nullable=True)
    avatar_path = Column(String, nullable=True)

    def __str__(self):
        return f"{self.last_name} {self.name}"