import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        "fastapi_graphql.main:init_app",
        host="localhost",
        port=8088,
        reload=True,
        # log_level="debug",
    )
