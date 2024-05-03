import time
from typing import Any, Callable, TypeVar

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers.auth import auth
from app.routers.todos import todos
from app.utilities.logger import logger

description = f"""
This is a simple Todo API built with FastAPI and MongoDB.

Authorize with GitHub OAuth at  <https://github.com/login/oauth/authorize?client_id={settings.GITHUB_OAUTH_CLIENT_ID}&redirect_uri=http://localhost:8000/v1/auth/callback>

## Usage

- **GET /todos**: Get all Todos
- **GET /todos/{id}**: Get a Todo
- **POST /todos**: Create a new Todo
- **PUT /todos/{id}**: Update a Todo
- **DELETE /todos/{id}**: Delete a Todo

"""

app = FastAPI(
    title="Todo API",
    description=description,
    version="0.1.0",
    docs_url="/",
    root_path=settings.ROOT_PATH,
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=[
        "http://localhost:3000",
    ],
)


F = TypeVar("F", bound=Callable[..., Any])


@app.middleware("http")
async def process_time_log_middleware(request: Request, call_next: F) -> Response:
    """
    Add API process time in response headers and log calls
    """
    start_time = time.time()
    response: Response = await call_next(request)
    process_time = str(round(time.time() - start_time, 3))
    response.headers["X-Process-Time"] = process_time

    logger.info(
        "Method=%s Path=%s StatusCode=%s ProcessTime=%s",
        request.method,
        request.url.path,
        response.status_code,
        process_time,
    )
    return response


app.include_router(
    todos.router,
    prefix="/v1/todos",
    tags=["todos"],
)
app.include_router(
    auth.router,
    prefix="/v1/auth",
    tags=["auth"],
)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True,
    )
