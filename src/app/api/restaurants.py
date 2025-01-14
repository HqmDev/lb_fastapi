from typing import List

from fastapi import APIRouter, HTTPException, Path

from app.api.models import RestaurantsDB, RestaurantSchema
from fastapi import APIRouter, HTTPException, Depends

from app.api.models import RestaurantSchema
from app.api import crud


router = APIRouter()


@router.post("/", response_model=RestaurantsDB, status_code=201)
async def create_restaurant(payload: RestaurantSchema):
    restaurant_id = await crud.post(payload)

    response_object = {
        "id": restaurant_id,
        "title": payload.title,
        "description": payload.description,
    }
    return response_object


@router.get("/{id}", response_model=RestaurantsDB)
async def read_restaurant(id: int = Path(..., gt=0),):
    restaurant = await crud.get(id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant


@router.get("/", response_model=List[RestaurantsDB])
async def read_all_restaurants():
    return await crud.get_all()


@router.put("/{id}/", response_model=RestaurantsDB)
async def update_restaurant(id: int, payload: RestaurantSchema):
    restaurant = await crud.get(id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    restaurant_id = await crud.put(id, payload)

    response_object = {
        "id": restaurant_id,
        "title": payload.title,
        "description": payload.description,
    }
    return response_object


@router.delete("/{id}/", response_model=RestaurantsDB)
async def delete_restaurant(id: int):
    restaurant = await crud.get(id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    await crud.delete(id)

    return restaurant
