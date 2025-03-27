from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_async_engine

from config import DATABASE_URL
from models import Base


async_engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionMaker = sessionmaker(async_engine)


async def create_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

