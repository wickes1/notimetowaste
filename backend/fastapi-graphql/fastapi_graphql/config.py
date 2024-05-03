import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


class DatabaseSession:

    def __init__(self, database_url=DATABASE_URL):
        self.engine = create_async_engine(database_url, echo=True)
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )
        self.session = None

    async def db_migrate_up(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def db_migrate_down(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)

    async def close(self):
        await self.engine.dispose()

    async def __aenter__(self) -> AsyncSession:
        self.session = self.SessionLocal()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def commit_rollback(self):
        try:
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get_session(self) -> AsyncSession:
        return self.session


db = DatabaseSession()
