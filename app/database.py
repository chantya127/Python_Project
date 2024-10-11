from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.your_database_name

items_collection = db.get_collection("items")
clockin_collection = db.get_collection("clock_in")
