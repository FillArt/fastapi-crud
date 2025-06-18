from pydantic import BaseModel, EmailStr
from typing import Optional

class ContactCreate(BaseModel):
    name: str
    age: int
    email: EmailStr
    institution: Optional[str]
    about: Optional[str]