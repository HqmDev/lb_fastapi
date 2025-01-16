from app.api.models import RestaurantSchema, UserCreate
from app.db import restaurants, database, users
from passlib.context import CryptContext


async def post(payload: RestaurantSchema):
    query = restaurants.insert().values(title=payload.title, description=payload.description)
    return await database.execute(query=query)


async def get(id: int):
    query = restaurants.select().where(id == restaurants.c.id)
    return await database.fetch_one(query=query)


async def get_all():
    query = restaurants.select()
    return await database.fetch_all(query=query)


async def put(id: int, payload: RestaurantSchema):
    query = (
        restaurants
        .update()
        .where(id == restaurants.c.id)
        .values(title=payload.title, description=payload.description)
        .returning(restaurants.c.id)
    )
    return await database.execute(query=query)


async def delete(id: int):
    query = restaurants.delete().where(id == restaurants.c.id)
    return await database.execute(query=query)


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user(payload: UserCreate):
    hashed_password = pwd_context.hash(payload.password)
    query = users.insert().values(
        username=payload.username,
        email=payload.email,
        hashed_password=hashed_password,
    )
    user_id = await database.execute(query)
    return {**payload.dict(), "id": user_id, "is_active": True}


async def get_user_by_id(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


async def get_user_by_email(email: str):
    query = users.select().where(users.c.email == email)
    return await database.fetch_one(query)