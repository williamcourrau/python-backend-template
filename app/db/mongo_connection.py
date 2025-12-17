from pymongo import MongoClient
from app.config import settings
from app.config.logging import get_logger
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

logger = get_logger(__name__)

# client = MongoClient(settings.MONGO_URI,
#                      serverSelectionTimeoutMS=5000,
#                      maxPoolSize=10)

# db = client[settings.MONGO_DB]

# def get_database():
#     return db

class MongoClientProvider:
    
    def __init__(self):
        logger.info("Initializing MongoDB client")
        self.client = AsyncIOMotorClient(
            settings.settings.MONGO_URI,
            serverSelectionTimeoutMS=5000,
            maxPoolSize=10,
        )
    
    def get_database(self) -> AsyncIOMotorDatabase:
        return self.client[settings.settings.MONGO_DB]