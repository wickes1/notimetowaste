from contextlib import asynccontextmanager
from fastapi import FastAPI
import strawberry
from fastapi_graphql.config import db
from fastapi_graphql.graphql.mutation import Mutation
from fastapi_graphql.graphql.query import Query
from strawberry.fastapi import GraphQLRouter


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting app")
    await db.db_migrate_up()
    yield
    print("Stopping app")
    await db.close()


def init_app() -> FastAPI:

    app = FastAPI(
        title="FastAPI GraphQL",
        description="FastAPI GraphQL",
        version="0.1.0",
        lifespan=lifespan,
    )

    @app.get("/")
    async def root():
        return {"message": "Hello World"}


    graphql_app = GraphQLRouter(schema=schema)

    app.include_router(graphql_app, prefix="/graphql")

    return app
schema = strawberry.Schema(query=Query, mutation=Mutation)
