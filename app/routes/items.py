import logging
from typing import Optional

from fastapi import APIRouter, HTTPException
from app.schemas.schemas import ItemModel, ItemResponse, DeleteResponse
from app.database import items_collection
from app.utils.generic_utils import serialize_mongo_data
from bson import ObjectId
from datetime import datetime
from http import HTTPStatus

router = APIRouter()


# --------------------------------------
# ITEM CRUD Operations
# --------------------------------------

@router.post("", response_model=ItemResponse)
async def create_item(item: ItemModel):
    item_data = item.dict()
    item_data["insert_date"] = datetime.now()  # Set current date as datetime

    # Ensure expiry_date is in datetime format (it's already defined as datetime in the model)
    item_data["expiry_date"] = item_data["expiry_date"].astimezone()

    new_item = await items_collection.insert_one(item_data)
    item_data["_id"] = str(new_item.inserted_id)  # Include the inserted ID
    data = serialize_mongo_data(item_data)
    item_response = ItemResponse(**data)
    return item_response


@router.get("/filter", response_model=list[ItemResponse])
async def filter_items(email: str = None, expiry_date: str = None, quantity: int = None):
    query = {}
    if email:
        query["email"] = email
    if expiry_date:
        query["expiry_date"] = {"$gt": datetime.strptime(expiry_date, '%Y-%m-%d')}
    if quantity is not None:
        query["quantity"] = {"$gte": quantity}

    items = await items_collection.find(query).to_list(100)
    # Ensure we serialize each item
    item_response_list: Optional[list[ItemResponse]] = []

    for item in items:
        data = serialize_mongo_data(item)
        item_response_list.append(ItemResponse(**data))
    return item_response_list


@router.get("/aggregation")
async def aggregate_items():
    pipeline = [
        {"$group": {"_id": "$email", "count": {"$sum": 1}}}
    ]
    result = await items_collection.aggregate(pipeline).to_list(None)
    return result


@router.get("/{id}", response_model=ItemResponse)
async def get_item(id: str):
    try:
        item = await items_collection.find_one({"_id": ObjectId(id)})
        if item:
            response = ItemResponse(**serialize_mongo_data(item))
            return response
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Item not found")
    except Exception as e:
        logging.exception(f" Following exception occurred while getting item{e}")
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Please try again later")


@router.put("/{id}", response_model=ItemResponse)
async def update_item(id: str, item: ItemModel):
    item_row = await items_collection.find_one({"_id": ObjectId(id)})
    if not item_row:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Item not found")

    update_data = item.dict(exclude_unset=True)  # Only update fields that were provided
    result = await items_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    updated_item = await items_collection.find_one({"_id": ObjectId(id)})

    item_response = ItemResponse(**serialize_mongo_data(updated_item))
    return item_response


@router.delete("/{id}", response_model=DeleteResponse)
async def delete_item(id: str):
    result = await items_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return {"msg": "Item deleted"}
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Item not found")
