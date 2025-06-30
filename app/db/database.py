from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.settings import settings

SQLALCHEMY_DATABASE_URL = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

async def get_db():
    async with async_session() as session:
        yield session


# def create_table():
#     Base.metadata.create_all(bind=engine)
