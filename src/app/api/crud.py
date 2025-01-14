from app.api.models import RestaurantSchema
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import restaurants, database


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