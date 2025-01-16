import os

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    create_engine
)
from sqlalchemy.sql import func

from databases import Database

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Restaurants table definition
restaurants = Table(
    "restaurants",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(50)),
    Column("description", String(50)),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)


# Users table definition
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(50), nullable=False, unique=True),
    Column("email", String(100), nullable=False, unique=True),
    Column("hashed_password", String(255), nullable=False),
    Column("is_active", Boolean, default=True),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
)

# databases query builder
database = Database(DATABASE_URL)