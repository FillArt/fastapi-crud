from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.params import File
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas import PostCreate
from app.schemas.posts import PostOut, PostUpdate, PostContentStatus
from app.services.posts import get_posts, create_post, get_post, delete_post, update_post, picture_upload, change_status

router = APIRouter()


@router.get("/", response_model=List[PostOut], tags=["Posts"], summary="Get all posts")
def read_posts(db: Session = Depends(get_db)):
    return get_posts(db)


@router.post("/", response_model=PostOut, tags=["Posts"], summary="Create a new post")
def create_new_post(post: PostCreate, db: Session = Depends(get_db)):
    return create_post(db, post)


@router.get("/{pk_id}", response_model=PostOut, tags=["Posts"], summary="Get post by ID")
def read_post(pk_id: int, db: Session = Depends(get_db)):
    post = get_post(db, pk_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post("/{pk_id}/upload", response_model=PostOut, tags=["Posts"], summary="Upload picture for post by ID")
async def upload_picture_by_id(pk_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    return await picture_upload(db, pk_id, file)


@router.delete("/{pk_id}", tags=["Posts"], summary="Delete a post by ID")
def delete_post_by_id(pk_id: int, db: Session = Depends(get_db)):
    post = delete_post(db, pk_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.patch("/{pk_id}", response_model=PostOut, tags=["Posts"], summary="Update a post by ID")
def update_post_by_id(pk_id: int, post: PostUpdate, db: Session = Depends(get_db)):
    updated_post = update_post(db, pk_id, post)
    if updated_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return updated_post


@router.patch("/{pk_id}/publish", response_model=PostOut, tags=["Posts"], summary="Update status post by ID")
def update_post_by_id(pk_id: int, post: PostContentStatus, db: Session = Depends(get_db)):
    updated_post = change_status(db, pk_id, post)
    if updated_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return updated_post

