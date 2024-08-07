from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.config import settings


def get_db() -> AsyncIOMotorDatabase:
    """
    Get MongoDB
    """
    if settings.TESTING:
        from mongomock_motor import AsyncMongoMockClient

        mock_db: AsyncIOMotorDatabase = AsyncMongoMockClient().todoDb
        return mock_db
    else:
        return AsyncIOMotorClient(settings.MONGO_URI).todoDb


db = get_db()
