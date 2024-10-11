from pydantic import BaseModel, field_validator, model_validator
from datetime import datetime
from typing import Optional


class ItemModel(BaseModel):
    email: str
    item_name: str
    quantity: int
    expiry_date: datetime  # Ensure this is datetime


class ItemResponse(ItemModel):
    insert_date: datetime  # Ensure this is datetime
    id: Optional[str] = None  # Include _id here



class ClockInModel(BaseModel):
    email: str
    location: str


class ClockInResponse(ClockInModel):
    insert_datetime: datetime  # Ensure this is datetime
    id: str  # Include _id here


class DeleteResponse(BaseModel):
    msg: str
