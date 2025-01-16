from pydantic import BaseModel, EmailStr


class RestaurantSchema(BaseModel):
    title: str
    description: str


class RestaurantsDB(RestaurantSchema):
    id: int


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True