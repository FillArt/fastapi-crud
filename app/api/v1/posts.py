from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.params import File
from sqlalchemy.orm import Session
from typing import List

from app.schemas.posts import PostOut, PostUpdate
from app.services.posts import get_posts, create_post, get_post, delete_post, update_post, picture_upload
from app.schemas import PostCreate
from app.db.database import get_db

router = APIRouter()

@router.get("/", response_model=List[PostOut], tags=["Posts"], summary="Get all posts")
def read_posts(db: Session = Depends(get_db)):
    return get_posts(db)

@router.post("/", response_model=PostOut, tags=["Posts"], summary="Create a new post")
def create_new_post(post: PostCreate, db: Session = Depends(get_db)):
    return create_post(db, post)

@router.get("/{id}", response_model=PostOut, tags=["Posts"], summary="Get post by ID")
def read_post(id: int, db: Session = Depends(get_db)):
    post = get_post(db, id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.post("/{id}/upload", response_model=PostOut, tags=["Posts"], summary="Upload picture for post by ID")
async def upload_picture_by_id(id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    return await picture_upload(db, id, file)

@router.delete("/{id}", tags=["Posts"], summary="Delete a post by ID")
def delete_post_by_id(id: int, db: Session = Depends(get_db)):
    post = delete_post(db, id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{id}", response_model=PostOut, tags=["Posts"], summary="Update a post by ID")
def update_post_by_id(id: int, post: PostUpdate, db: Session = Depends(get_db)):
    updated_post = update_post(db, id, post)
    if updated_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return updated_post