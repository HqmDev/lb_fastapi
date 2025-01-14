from app.api.models import RestaurantSchema
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import Restaurants


async def create_restaurant(db: AsyncSession, title: str, description: str):
    new_restaurant = Restaurants(title=title, description=description)
    db.add(new_restaurant)
    await db.commit()
    await db.refresh(new_restaurant)
    return new_restaurant


async def get_restaurant(db: AsyncSession, restaurant_id: int):
    result = await db.execute(select(Restaurants).where(Restaurants.id == restaurant_id))
    return result.scalars().first()


async def get_all_restaurants(db: AsyncSession):
    result = await db.execute(select(Restaurants))
    return result.scalars().all()


async def update_restaurant(db: AsyncSession, restaurant_id: int, title: str, description: str):
    result = await db.execute(select(Restaurants).where(Restaurants.id == restaurant_id))
    restaurant = result.scalars().first()
    if restaurant:
        restaurant.title = title
        restaurant.description = description
        await db.commit()
        await db.refresh(restaurant)
    return restaurant


async def delete_restaurant(db: AsyncSession, restaurant_id: int):
    result = await db.execute(select(Restaurants).where(Restaurants.id == restaurant_id))
    restaurant = result.scalars().first()
    if restaurant:
        await db.delete(restaurant)
        await db.commit()
    return restaurant