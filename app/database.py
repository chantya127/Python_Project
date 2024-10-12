from motor.motor_asyncio import AsyncIOMotorClient
from starlette.config import Config

config = Config()
MONGO_URI = config("MONGO_URI", cast=str, default=None)
client = AsyncIOMotorClient(MONGO_URI)
db = client.your_database_name

items_collection = db.get_collection("items")
clockin_collection = db.get_collection("clock_in")
