from datetime import datetime

from bson import ObjectId


def serialize_mongo_data(data):
    if isinstance(data, list):
        return [serialize_mongo_data(item) for item in data]
    if isinstance(data, dict):
        data["id"] = str(data["_id"])  # Convert ObjectId to string
        for key, value in data.items():
            if isinstance(value, (datetime)):
                data[key] = value.isoformat()  # Convert datetime to ISO format
    return data
