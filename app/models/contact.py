from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String, nullable=False, index=True)
    institution = Column(String, nullable=True)
    about = Column(String, nullable=True)
    file_path = Column(String, nullable=True)

