import logging
import sys
import time
from datetime import UTC, datetime
from typing import Any, Callable, TypeVar

import uvicorn
from bson import ObjectId
from fastapi import FastAPI, HTTPException, Path, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


# Use settings class instead of os.environ
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    ROOT_PATH: str = ""
    LOGGING_LEVEL: str = "INFO"
    MONGO_URI: str


settings = Settings()

logging.basicConfig(
    stream=sys.stdout,
    level=settings.LOGGING_LEVEL,
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",  # noqa: E501
    datefmt="%d/%b/%Y %H:%M:%S",
)
logger = logging.getLogger("my-todos")

db_client = AsyncIOMotorClient(settings.MONGO_URI)
db = db_client.todoDb

description = """
This is a simple Todo API built with FastAPI and MongoDB.

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


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=[
        "http://localhost:3000",
    ],
)


class Todo(BaseModel):
    title: str
    completed: bool = False


class TodoId(BaseModel):
    id: str


class TodoRecord(
    TodoId,
    Todo,
):
    created_date: datetime
    updated_date: datetime


@app.get("/")
async def read_root() -> dict[str, str]:
    """
    Hello World
    """
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: str) -> dict[str, str]:
    """
    Get an Item
    """
    return {"item_id": item_id}


@app.post("/todos", response_model=TodoId)
async def create_todo(payload: Todo) -> TodoId:
    """
    Create a new Todo
    """
    now = datetime.now(UTC)
    insert_result = await db.todos.insert_one(
        {
            "title": payload.title,
            "completed": payload.completed,
            "created_date": now,
            "updated_date": now,
        }
    )

    return TodoId(id=str(insert_result.inserted_id))


@app.get("/todos", response_model=list[TodoRecord])
async def get_todos() -> list[TodoRecord]:
    """
    Get all Todos
    """
    todos: list[TodoRecord] = []
    async for doc in db.todos.find():
        todos.append(
            TodoRecord(
                id=str(doc["_id"]),
                title=doc["title"],
                completed=doc["completed"],
                created_date=doc["created_date"],
                updated_date=doc["updated_date"],
            )
        )

    return todos


class NotFoundException(BaseModel):
    detail: str = "Not Found"


MONGO_ID_REGEX = r"^[a-f\d]{24}$"


@app.get(
    "/todos/{id}",
    response_model=TodoRecord,
    responses={
        404: {
            "description": "Not Found, response description in Open API Docs",
            "model": NotFoundException,
        }
    },
)
async def get_todo(
    id: str = Path(description="Todo ID", pattern=MONGO_ID_REGEX)
) -> TodoRecord:
    """
    Get a Todo
    """
    doc = await db.todos.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Todo not found")

    return TodoRecord(
        id=str(doc["_id"]),
        title=doc["title"],
        completed=doc["completed"],
        created_date=doc["created_date"],
        updated_date=doc["updated_date"],
    )


@app.put(
    "/todos/{id}",
    response_model=TodoId,
    responses={404: {"description": "Not Found", "model": NotFoundException}},
)
async def update_todo(
    payload: Todo,
    id: str = Path(description="Todo ID", pattern=MONGO_ID_REGEX),
) -> TodoId:
    """
    Update a Todo
    """
    now = datetime.now(UTC)
    update_result = await db.todos.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "title": payload.title,
                "completed": payload.completed,
                "updated_date": now,
            }
        },
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found")

    return TodoId(id=id)


@app.delete(
    "/todos/{id}",
    response_model=TodoId,
    responses={404: {"description": "Not Found", "model": NotFoundException}},
)
async def delete_todo(
    id: str = Path(description="Todo ID", pattern=MONGO_ID_REGEX)
) -> TodoId:
    """
    Delete a Todo
    """
    delete_result = await db.todos.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found")

    return TodoId(id=id)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True,
    )
