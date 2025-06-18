from fastapi import APIRouter
from app.crud.posts import get_posts, create_post, get_post, delete_post, update_post

router = APIRouter()

router.get("/", tags=["Posts"], summary="Get all posts")(get_posts)
router.post("/", tags=["Posts"], summary="Create a new post")(create_post)
router.get("/{id}", tags=["Posts"], summary="Get post by ID")(get_post)
router.delete("/{id}", tags=["Posts"], summary="Delete a post by ID")(delete_post)
router.put("/{id}", tags=["Posts"], summary="Update a post by ID")(update_post)