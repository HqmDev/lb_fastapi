import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    create_engine
)
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

from databases import Database

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()
Base = declarative_base()

# Create the async SQLAlchemy engine
async_engine = create_async_engine(DATABASE_URL, echo=True)

# Async session maker
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


class Restaurants(Base):
    __tablename__ = "restaurants"
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    description = Column(String(50))
    created_date = Column(DateTime, server_default=func.now(), nullable=False)


# databases query builder
# Dependency for getting an async database session
async def get_async_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


# Asynchronous function to create tables at startup
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

database = Database(DATABASE_URL)
