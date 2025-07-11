import os
from contextlib import asynccontextmanager

from fastapi.staticfiles import StaticFiles

from fastapi import FastAPI

from app.routes.v1 import posts, contact, categories, content, author
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine

from fastapi_pagination import add_pagination
from app.admin.views import setup_admin


import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # сюда можно добавить код на shutdown, если нужно

app = FastAPI(lifespan=lifespan)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")


origins = [
    "http://localhost:4321",
    "http://127.0.0.1:4321",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(author.router, prefix="/routes/v1/author", tags=["Authors"])
app.include_router(categories.router, prefix="/routes/v1/categories", tags=["Categories"])
app.include_router(posts.router, prefix="/routes/v1/posts", tags=["Posts"])
app.include_router(content.router, prefix="/routes/v1/content", tags=["Content"])
app.include_router(contact.router, prefix="/routes/v1/contact", tags=["Contact"])

add_pagination(app)
setup_admin(app, engine)

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
