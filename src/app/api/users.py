from fastapi import APIRouter, HTTPException
from app.api.models import UserCreate, UserOut
from app.api import crud

router = APIRouter()


@router.post("/", response_model=UserOut, status_code=201)
async def create_user(payload: UserCreate):
    existing_user = await crud.get_user_by_email(payload.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(payload)


@router.get("/{user_id}/", response_model=UserOut)
async def get_user(user_id: int):
    user = await crud.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user