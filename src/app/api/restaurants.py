from typing import List

from fastapi import APIRouter, HTTPException, Path

from app.api import crud
from app.api.models import RestaurantsDB, RestaurantSchema
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.models import RestaurantSchema
from app.api import crud
from app.db import Restaurants
from app.db import get_async_db

router = APIRouter()


@router.post("/", response_model=Restaurants, status_code=201)
async def create_restaurant(payload: RestaurantSchema, db: AsyncSession = Depends(get_async_db)):
    return await crud.create_restaurant(db, title=payload.title, description=payload.description)


@router.get("/{id}", response_model=Restaurants)
async def read_restaurant(id: int, db: AsyncSession = Depends(get_async_db)):
    restaurant = await crud.get_restaurant(db, restaurant_id=id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant


@router.get("/", response_model=List[Restaurants])
async def read_all_restaurants(db: AsyncSession = Depends(get_async_db)):
    return await crud.get_all_restaurants(db)


@router.put("/{id}/", response_model=Restaurants)
async def update_restaurant(id: int, payload: RestaurantSchema, db: AsyncSession = Depends(get_async_db)):
    restaurant = await crud.update_restaurant(db, restaurant_id=id, title=payload.title, description=payload.description)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant


@router.delete("/{id}/", response_model=Restaurants)
async def delete_restaurant(id: int, db: AsyncSession = Depends(get_async_db)):
    restaurant = await crud.delete_restaurant(db, restaurant_id=id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant
# @router.post("/", response_model=RestaurantsDB, status_code=201)
# async def create_restaurant(payload: RestaurantSchema):
#     restaurant_id = await crud.post(payload)
#
#     response_object = {
#         "id": restaurant_id,
#         "title": payload.title,
#         "description": payload.description,
#     }
#     return response_object
#
#
# @router.get("/{id}", response_model=RestaurantsDB)
# async def read_restaurant(id: int = Path(..., gt=0),):
#     restaurant = await crud.get(id)
#     if not restaurant:
#         raise HTTPException(status_code=404, detail="Restaurant not found")
#     return restaurant
#
#
# @router.get("/", response_model=List[RestaurantsDB])
# async def read_all_restaurants():
#     return await crud.get_all()
#
#
# @router.put("/{id}/", response_model=RestaurantsDB)
# async def update_restaurant(id: int, payload: RestaurantSchema):
#     restaurant = await crud.get(id)
#     if not restaurant:
#         raise HTTPException(status_code=404, detail="Restaurant not found")
#
#     restaurant_id = await crud.put(id, payload)
#
#     response_object = {
#         "id": restaurant_id,
#         "title": payload.title,
#         "description": payload.description,
#     }
#     return response_object
#
#
# @router.delete("/{id}/", response_model=RestaurantsDB)
# async def delete_restaurant(id: int):
#     restaurant = await crud.get(id)
#     if not restaurant:
#         raise HTTPException(status_code=404, detail="Restaurant not found")
#
#     await crud.delete(id)
#
#     return restaurant