from typing import AsyncGenerator

import pytest
from httpx import AsyncClient

from app.deps import get_vector_store
from app.provider import ExtendedPgVector


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: backend name.
    """
    return "asyncio"


@pytest.fixture
async def fake_vector_store() -> ExtendedPgVector:
    return ExtendedPgVector(
        connection_string="postgresql://postgres:postgres@localhost:5433/test",
        collection_name="testcollection",
        embedding_function=None,
    )


@pytest.fixture
async def fastapi_app():
    from app.main import app

    # app.dependency_overrides[get_vector_store] = lambda: fake_vector_store
    return app


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture that creates client for requesting server.

    :param fastapi_app: the application.
    :yield: client for the app.
    """
    from app.main import app

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
