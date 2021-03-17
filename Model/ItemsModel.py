from pydantic import BaseModel
from typing import Optional


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = False


class Items(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    is_member: Optional[bool] = False



