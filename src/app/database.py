import logging

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError
from pymongo.server_api import ServerApi

from src.config import settings

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDBMotorClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        database_url = settings.MONGO_URI
        database_name = settings.MONGO_DB_NAME

        if not database_url or not database_name:
            raise ValueError("MongoDB URI or database name is missing from environment variables.")

        # Connect to MongoDB using the URI and database name
        self.client = AsyncIOMotorClient(database_url, server_api=ServerApi('1'))
        self.db = self.client.get_database(database_name)

    async def ping_server(self):
        """
        Pings the MongoDB server to check if the connection is active.
        """
        try:
            await self.client.admin.command('ping')
            logger.info("Successfully connected to MongoDB!")
        except ServerSelectionTimeoutError:
            logger.error("Could not connect to MongoDB. Server selection timed out.")
        except Exception as e:
            logger.error(f"Something went wrong: {e}")

    def get_collection(self, collection_name: str):
        """
        Get the collection instance from the database.
        """
        return self.db.get_collection(collection_name)
