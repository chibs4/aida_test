from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
import uvicorn

from settings import settings
from routes import router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)
app.include_router(router)

register_tortoise(
    app,
    db_url=str(settings.POSTGRES_URI),
    modules={"model": ["model"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == "__main__":
    uvicorn.run(app=app, host=settings.SERVER_HOST, port=settings.SERVER_PORT)
