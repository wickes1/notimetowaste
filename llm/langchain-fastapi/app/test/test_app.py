import pytest
from fastapi import FastAPI
from httpx import AsyncClient


@pytest.mark.anyio
async def test_documents(client: AsyncClient, fastapi_app: FastAPI):
    url = fastapi_app.url_path_for("add_documents")
    response = await client.post(
        url,
        json=[
            {"page_content": "This is a test document", "metadata": {"author": "test"}}
        ],
    )
    assert response.status_code == 201


@pytest.mark.anyio
async def test_chat(client: AsyncClient, fastapi_app: FastAPI):
    url = fastapi_app.url_path_for("chat")
    response = await client.post(url, params={"msg": "What is the capital of France?"})
    assert response.status_code == 200
