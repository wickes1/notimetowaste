from datetime import UTC, datetime
from typing import Annotated

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.constant import MONGO_ID_REGEX
from app.routers.auth.auth import validate_access_token
from app.utilities.db import db

from .models import NotFoundException, Todo, TodoId, TodoRecord, UnauthorizedException

security = HTTPBearer()
router = APIRouter()


@router.post(
    "", response_model=TodoId, responses={401: {"description": "Unauthorized"}}
)
async def create_todo(
    access_token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user: Annotated[str, Depends(validate_access_token)],
    payload: Todo,
) -> TodoId:
    """
    Create a new Todo
    """
    now = datetime.now(UTC)
    insert_result = await db.todos.insert_one(
        {
            "user": user,
            "title": payload.title,
            "completed": payload.completed,
            "created_date": now,
            "updated_date": now,
        }
    )

    return TodoId(id=str(insert_result.inserted_id))


@router.get(
    "",
    response_model=list[TodoRecord],
    responses={
        401: {"description": "Unauthorized", "model": UnauthorizedException},
    },
)
async def get_todos(
    access_token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user: Annotated[str, Depends(validate_access_token)],
) -> list[TodoRecord]:
    """
    Get all Todos
    """
    todos: list[TodoRecord] = []
    async for doc in db.todos.find({"user": user}):
        todos.append(
            TodoRecord(
                user=doc["user"],
                id=str(doc["_id"]),
                title=doc["title"],
                completed=doc["completed"],
                created_date=doc["created_date"],
                updated_date=doc["updated_date"],
            )
        )

    return todos


@router.get(
    "/{id}",
    response_model=TodoRecord,
    responses={
        401: {"description": "Unauthorized", "model": UnauthorizedException},
        404: {"description": "Not Found", "model": NotFoundException},
    },
)
async def get_todo(
    access_token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user: Annotated[str, Depends(validate_access_token)],
    id: str = Path(description="Todo ID", pattern=MONGO_ID_REGEX),
) -> TodoRecord:
    """
    Get a Todo
    """
    doc = await db.todos.find_one({"_id": ObjectId(id), "user": user})
    if not doc:
        raise HTTPException(status_code=404, detail="Todo not found")

    return TodoRecord(
        user=doc["user"],
        id=str(doc["_id"]),
        title=doc["title"],
        completed=doc["completed"],
        created_date=doc["created_date"],
        updated_date=doc["updated_date"],
    )


@router.put(
    "/{id}",
    response_model=TodoId,
    responses={
        401: {"description": "Unauthorized", "model": UnauthorizedException},
        404: {"description": "Not Found", "model": NotFoundException},
    },
)
async def update_todo(
    access_token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user: Annotated[str, Depends(validate_access_token)],
    payload: Todo,
    id: str = Path(description="Todo ID", pattern=MONGO_ID_REGEX),
) -> TodoId:
    """
    Update a Todo
    """
    now = datetime.now(UTC)
    update_result = await db.todos.update_one(
        {"_id": ObjectId(id), "user": user},
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


@router.delete(
    "/{id}",
    response_model=TodoId,
    responses={
        401: {"description": "Unauthorized", "model": UnauthorizedException},
        404: {"description": "Not Found", "model": NotFoundException},
    },
)
async def delete_todo(
    access_token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user: Annotated[str, Depends(validate_access_token)],
    id: str = Path(description="Todo ID", pattern=MONGO_ID_REGEX),
) -> TodoId:
    """
    Delete a Todo
    """
    delete_result = await db.todos.delete_one({"_id": ObjectId(id), "user": user})

    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found")

    return TodoId(id=id)
