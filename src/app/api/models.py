from pydantic import BaseModel


class RestaurantSchema(BaseModel):
    title: str
    description: str


class RestaurantsDB(RestaurantSchema):
    id: int