from fastapi import APIRouter, HTTPException
from app.schemas.schemas import ClockInModel, ClockInResponse, DeleteResponse
from app.database import clockin_collection
from app.utils.generic_utils import serialize_mongo_data
from bson import ObjectId
from datetime import datetime
from http import HTTPStatus

router = APIRouter()


# --------------------------------------
# CLOCK-IN CRUD Operations
# --------------------------------------

@router.post("", response_model=ClockInResponse)
async def create_clockin(clockin: ClockInModel):
    clockin_data = clockin.dict()
    clockin_data["insert_datetime"] = datetime.utcnow()  # Insert current datetime for clock-in

    new_clockin = await clockin_collection.insert_one(clockin_data)
    clockin_data["_id"] = str(new_clockin.inserted_id)  # Include the inserted ID
    return serialize_mongo_data(clockin_data)  # Return the complete clock-in data


@router.get("/filter", response_model=list[ClockInResponse])
async def filter_clockins(email: str = None, location: str = None, after_date: str = None):
    query = {}
    if email:
        query["email"] = email
    if location:
        query["location"] = location
    if after_date:
        query["insert_datetime"] = {"$gt": datetime.strptime(after_date, '%Y-%m-%d')}

    clockins = await clockin_collection.find(query).to_list(100)
    return [serialize_mongo_data(clockin) for clockin in clockins]  # Ensure we serialize each clock-in


@router.get("/{id}", response_model=ClockInResponse)
async def get_clockin(id: str):
    try:
        clockin = await clockin_collection.find_one({"_id": ObjectId(id)})
        if clockin:
            return serialize_mongo_data(clockin)  # Ensure we serialize the clock-in
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Clock-in record not found")
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))


@router.put("/{id}", response_model=ClockInResponse)
async def update_clockin(id: str, clockin: ClockInModel):
    clockin_record = await clockin_collection.find_one({"_id": ObjectId(id)})
    if not clockin_record:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Clock-in record not found")

    update_data = clockin.dict(exclude_unset=True)  # Only update fields that were provided
    result = await clockin_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    updated_clockin = await clockin_collection.find_one({"_id": ObjectId(id)})
    return serialize_mongo_data(updated_clockin)  # Return the updated clock-in


@router.delete("/{id}", response_model=DeleteResponse)
async def delete_clockin(id: str):
    result = await clockin_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return {"msg": "Clock-in deleted"}
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Clock-in record not found")
