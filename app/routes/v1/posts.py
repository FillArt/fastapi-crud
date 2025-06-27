from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.params import File
from fastapi_pagination import paginate, Page
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas import PostCreate
from app.schemas.posts import PostOut, PostUpdate, PostContentStatus
from app.services.posts import get_posts_service, create_post_service, get_post_service, delete_post_service, \
    update_post_service, picture_upload_service, change_status_service, update_picture_post_service

router = APIRouter()

@router.get("/", response_model=Page[PostOut], tags=["Posts"], summary="Get all posts")
def read_posts(db: Session = Depends(get_db)):
    return paginate(get_posts_service(db))


@router.post("/", response_model=PostOut, tags=["Posts"], summary="Create a new post")
def create_new_post(post: PostCreate, db: Session = Depends(get_db)):
    return create_post_service(db, post)


@router.get("/{id}", response_model=PostOut, tags=["Posts"], summary="Get post by ID")
def read_post(id: int, db: Session = Depends(get_db)):
    return get_post_service(db, id)

@router.post("/{id}/upload", response_model=PostOut, tags=["Posts"], summary="Upload picture for post by ID")
async def upload_picture_by_id(id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    return await picture_upload_service(db, id, file)


@router.delete("/{id}", tags=["Posts"], summary="Delete a post by ID")
def delete_post_by_id(id: int, db: Session = Depends(get_db)):
    return delete_post_service(db, id)

@router.patch("/{id}", response_model=PostOut, tags=["Posts"], summary="Update a post by ID")
def update_post_by_id(id: int, post: PostUpdate, db: Session = Depends(get_db)):
    return update_post_service(db, id, post)

@router.patch("/{id}/publish", response_model=PostOut, tags=["Posts"], summary="Update status post by ID")
def update_status_by_id(id: int, post: PostContentStatus, db: Session = Depends(get_db)):
    return change_status_service(db, id, post)

@router.patch("/{id}/upload", response_model=PostOut, tags=["Posts"], summary="Update picture for post by ID")
async def update_picture_by_id(id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    return await update_picture_post_service(db, id, file)
