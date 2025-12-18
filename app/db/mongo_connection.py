from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import (
    ServerSelectionTimeoutError,
    ConfigurationError,
    OperationFailure,
    ConnectionFailure,
)

from app.config.settings import settings
from app.config.logging import get_logger

logger = get_logger(__name__)


class MongoClientProvider:
    """
    Provides a validated MongoDB database connection.

    This class ensures that:
    - MongoDB connectivity is verified at startup
    - Configuration issues fail fast
    - Errors are reported in a user-friendly manner
    """

    def __init__(self):
        logger.info("Initializing MongoDB client")

        try:
            self.client = AsyncIOMotorClient(
                settings.MONGO_URI,
                serverSelectionTimeoutMS=5000,
            )

        except ConfigurationError as e:
            logger.exception("Invalid MongoDB configuration")
            raise RuntimeError(
                "Database configuration is invalid. "
                "Please contact support to verify system settings."
            ) from e

        except Exception as e:
            logger.exception("Unexpected error during MongoDB client initialization")
            raise RuntimeError(
                "Unexpected error while initializing database connection."
            ) from e

    async def get_database(self) -> AsyncIOMotorDatabase:
        """
        Returns a validated MongoDB database instance.

        Raises:
            RuntimeError: If the database is unreachable or authentication fails.
        """
        try:
            # Force connection check
            await self.client.admin.command("ping")
            logger.info("MongoDB connection established successfully")

            return self.client[settings.MONGO_DB]

        except ServerSelectionTimeoutError as e:
            logger.error("MongoDB server is unreachable", exc_info=e)
            raise RuntimeError(
                "The system cannot connect to the database at this time. "
                "Please try again later."
            ) from e

        except OperationFailure as e:
            logger.error("MongoDB authentication failed", exc_info=e)
            raise RuntimeError(
                "Database authentication failed. "
                "Please contact support."
            ) from e

        except ConnectionFailure as e:
            logger.error("MongoDB connection failure", exc_info=e)
            raise RuntimeError(
                "A database connection error occurred. "
                "Please try again later."
            ) from e

        except Exception as e:
            logger.exception("Unexpected database error")
            raise RuntimeError(
                "An unexpected database error occurred. "
                "No data was lost."
            ) from e
