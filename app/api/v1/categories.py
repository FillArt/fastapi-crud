from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.category import CategoryOut, CategoryCreate
from app.services.categories import create_category

router = APIRouter()

@router.post("/", response_model=CategoryOut, tags=["Categories"])
async def create_category_post(category: CategoryCreate , db: Session = Depends(get_db)):
    return create_category(db, category)