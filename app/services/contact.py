from app.schemas.contact import ContactCreate
from app.models import Contact
from sqlalchemy.orm import Session

def contact_create(db: Session, request: ContactCreate):
    contact_instance = Contact(**request.dict())
    db.add(contact_instance)
    db.commit()
    db.refresh(contact_instance)
    return contact_instance

def get_all_contacts(db: Session):
    return db.query(Contact).all()