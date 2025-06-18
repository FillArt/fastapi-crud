from fastapi import FastAPI
from app.api.v1 import posts
import uvicorn

app = FastAPI()

app.include_router(posts.router, prefix="/api/v1/posts", tags=["Posts"])

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
